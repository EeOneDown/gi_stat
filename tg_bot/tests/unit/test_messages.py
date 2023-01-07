import unittest

from tg_bot.messages import BotRegexps


class BotRegexpsTestCase(unittest.TestCase):
    def test_follow_character(self):
        good_messages = [
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя (АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ)",
            "АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя 1 2 3",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ 10 11 12",
            "АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ 22 34 80",
        ]
        for good_message in good_messages:
            self.assertTrue(BotRegexps.FOLLOW_CHARACTER.search(good_message))
            self.assertTrue(BotRegexps.FOLLOW_CHARACTER.match(good_message).groupdict()["name"])

        bad_messages = [
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя абвгдеёжзийклмнопрстуфхцчшщъыьэюя-абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
            "abcdefghijklmnopqrstuvwxyz",
            "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "ABCDEFGHIJKLMnopqrstuvwxyz-abcdefghijklmNOPQRSTUVWXYZ",
            "абвгдеёжзийклмнопрстуфхцчшщъыьэюя 111 222 3333",
            "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ -10 11 12",
            "АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ 22 +34 80",
        ]
        for bad_message in bad_messages:
            self.assertFalse(BotRegexps.FOLLOW_CHARACTER.search(bad_message))

        text = "АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ 2 14 80"
        name, talents = BotRegexps.parse_follow_message(text)
        self.assertEqual(name, "АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ")
        self.assertDictEqual(talents, {"normal_attack": 2, "elemental_skill": 14, "elemental_burst": 15})

    def test_unfollow_character(self):
        good_messages = [
            "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
            "-абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
            "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя (АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ)",
            "- АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ",
        ]
        for good_message in good_messages:
            self.assertTrue(BotRegexps.UNFOLLOW_CHARACTER.search(good_message))

        bad_messages = [
            "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя абвгдеёжзийклмнопрстуфхцчшщъыьэюя-абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
            "- abcdefghijklmnopqrstuvwxyz",
            "- abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "- ABCDEFGHIJKLMnopqrstuvwxyz-abcdefghijklmNOPQRSTUVWXYZ",
            "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя 111 222 3333",
            "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ -10 11 12",
            "АБВГДЕЁЖЗИЙКЛМНОпрстуфхцчшщъыьэюя-абвгдеёжзийклмноПРСТУФХЦЧШЩЪЫЬЭЮЯ 22 +34 80",
        ]
        for bad_message in bad_messages:
            self.assertFalse(BotRegexps.UNFOLLOW_CHARACTER.search(bad_message))

        text = "- абвгдеёжзийклмнопрстуфхцчшщъыьэюя (АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ)"
        name = BotRegexps.parse_unfollow_message(text)
        self.assertEqual(name, "абвгдеёжзийклмнопрстуфхцчшщъыьэюя (АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ)")

    def test_character_talents(self):
        good_messages = ["1 2 3", "11 22 33", "0 0 0"]
        for good_message in good_messages:
            self.assertTrue(BotRegexps.CHARACTER_TALENTS.search(good_message))

        bad_messages = ["-1 -2 -3", "111 222 333"]
        for bad_message in bad_messages:
            self.assertFalse(BotRegexps.CHARACTER_TALENTS.search(bad_message))

        text = "1 22 13"
        talents = BotRegexps.parse_character_talents_message(text)
        self.assertDictEqual(talents, {"normal_attack": 1, "elemental_skill": 15, "elemental_burst": 13})
