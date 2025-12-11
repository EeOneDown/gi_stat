import unittest
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from tg_bot import parsers


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


class ParsersTestCase(unittest.TestCase):
    def setUp(self):
        parsers.temp_characters.clear()
        parsers.temp_talent.clear()
        parsers.temp_weekly_bosses.clear()

    def test_get_characters_list(self):
        # Use real string names to match data and avoid MagicMock .name behavior.
        char1 = MagicMock()
        char1.name = "Айно"
        char2 = MagicMock()
        char2.name = "Аль-Хайтам"
        chars = [char1, char2]
        queryset = MagicMock()
        queryset.order_by.return_value.all.return_value = chars
        with patch.object(parsers, "Character") as character_mock:
            character_mock.objects = queryset
            self.assertEqual(parsers.get_characters_list(), ["Айно", "Аль-Хайтам"])
            queryset.order_by.assert_called_once_with("release_date")

    @patch("tg_bot.parsers.add_new_character")
    @patch("tg_bot.parsers.get_characters_list", return_value=["Known"])
    @patch("tg_bot.parsers.parsing")
    def test_sync_characters_adds_only_new(self, parsing_mock, get_list_mock, add_char_mock):
        html = """
        <table class="article-table">
          <tbody>
            <tr></tr>
            <tr><td></td><td><a title="Known" href="/known"></a></td></tr>
            <tr><td></td><td><a title="NewChar" href="/new-char"></a></td></tr>
          </tbody>
        </table>
        """
        parsing_mock.return_value = _soup(html)

        parsers.sync_characters()

        add_char_mock.assert_called_once_with("NewChar", "/new-char")
        get_list_mock.assert_called_once()
        parsing_mock.assert_called_once()

    @patch("tg_bot.parsers.Character")
    @patch("tg_bot.parsers.parse_weekly_boss", return_value="Azhdaha")
    @patch("tg_bot.parsers.parse_talent_domain", return_value=("Forsaken Rift", "Понедельник, четверг"))
    @patch("tg_bot.parsers.parsing")
    def test_add_new_character_creates_character(
        self, parsing_mock, parse_talent_mock, parse_boss_mock, character_mock
    ):
        html = """
        <div class="pi-item"><h3>Дата релиза</h3><div class="pi-data-value">1 января 2024 (UTC+3)</div></div>
        <span id="Повышение_уровня_талантов"></span>
        <table><tbody>
          <tr><td></td><td></td><td><a href="/talent"></a></td><td><a href="/boss"></a></td></tr>
        </tbody></table>
        """
        parsing_mock.return_value = _soup(html)

        parsers.add_new_character("Лайла", "/href")

        # character instance should be created with parsed fields
        character_mock.assert_called_once()
        instance = character_mock.call_args.kwargs
        self.assertEqual(instance["name"], "Лайла")
        self.assertEqual(instance["talent_domain"], "Forsaken Rift")
        self.assertEqual(instance["weekly_boss"], "Azhdaha")
        self.assertEqual(instance["talent_days"], 1)
        character_mock.return_value.save.assert_not_called()
        parse_talent_mock.assert_called_once_with("/talent")
        parse_boss_mock.assert_called_once_with("/boss")

    @patch("tg_bot.parsers.Character")
    @patch("tg_bot.parsers.parse_weekly_boss", return_value="Azhdaha")
    @patch("tg_bot.parsers.parse_talent_domain", return_value=("Forsaken Rift", "Понедельник, четверг"))
    @patch("tg_bot.parsers.parsing")
    def test_add_new_character_reuses_cached_values(
        self, parsing_mock, parse_talent_mock, parse_boss_mock, character_mock
    ):
        html = """
        <div class="pi-item"><h3>Дата релиза</h3><div class="pi-data-value">1 января 2024 (UTC+3)</div></div>
        <span id="Повышение_уровня_талантов"></span>
        <table><tbody>
          <tr><td></td><td></td><td><a href="/talent"></a></td><td><a href="/boss"></a></td></tr>
        </tbody></table>
        """
        soup = _soup(html)
        parsing_mock.side_effect = [soup, soup]

        parsers.add_new_character("Лайла", "/href")
        parsers.add_new_character("Лайла 2", "/href-2")

        # Domain/boss parsers called once because results cached by href.
        parse_talent_mock.assert_called_once_with("/talent")
        parse_boss_mock.assert_called_once_with("/boss")

    @patch("tg_bot.parsers.parsing")
    def test_parse_talent_domain(self, parsing_mock):
        html = """
        <div class="pi-data-value">Domain (Понедельник, четверг)</div>
        <div class="pi-data-value">Ignore me</div>
        """
        parsing_mock.return_value = _soup(html)

        domain, days = parsers.parse_talent_domain("/talent")

        self.assertEqual(domain, "Domain ")
        self.assertEqual(days, "Понедельник, четверг")
        parsing_mock.assert_called_once_with("/talent")

    @patch("tg_bot.parsers.parsing")
    def test_parse_weekly_boss_with_span(self, parsing_mock):
        html = """
        <div class="pi-data-value"><span>Райден</span></div>
        """
        parsing_mock.return_value = _soup(html)

        boss = parsers.parse_weekly_boss("/boss")

        self.assertEqual(boss, "Райден")
        parsing_mock.assert_called_once_with("/boss")

    @patch("tg_bot.parsers.requests.get")
    def test_parsing_builds_base_url_and_returns_soup(self, get_mock):
        response = MagicMock()
        response.text = "<html><body>ok</body></html>"
        response.raise_for_status.return_value = None
        get_mock.return_value = response

        soup = parsers.parsing("/path")

        get_mock.assert_called_once()
        called_url = get_mock.call_args.kwargs["url"]
        self.assertTrue(called_url.startswith(parsers.base_url))
        self.assertEqual(soup.find("body").text, "ok")

    @patch("tg_bot.parsers.time.sleep")
    @patch("tg_bot.parsers.requests.get", side_effect=Exception("boom"))
    def test_parsing_retries_and_raises(self, get_mock, sleep_mock):
        with self.assertRaises(Exception):
            parsers.parsing("/fail")
        self.assertEqual(get_mock.call_count, 5)
        sleep_mock.assert_called()


if __name__ == "__main__":
    unittest.main()
