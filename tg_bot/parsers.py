import time

import dateparser

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from tg_bot.models import Character
from tg_bot.models import Days
from datetime import timezone


# ua = UserAgent().random
base_url = 'https://genshin-impact.fandom.com'


def get_characters_list() -> list[str]:
    characters_list = list(Character.objects.order_by("release_date").all())
    return [char.name for char in characters_list]

def sync_characters() -> None:

    result = {}

    soup = parsing('/ru/wiki/%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8')

    characters_temp = soup.find('table', class_='article-table').find('tbody').find_all('tr')
    for character in characters_temp[1:]:
        char_stats = character.find_all('td')[1].find('a')
        result[char_stats.get('title')] = char_stats.get('href')

    characters_list = get_characters_list()

    for char, href in result.items():
        if char not in characters_list:
            add_new_character(char, href)

def add_new_character(name: str, href: str) -> None:
    soup = parsing(href)

    data_table = soup.find_all('div', class_='pi-item')

    row_realise_date = None

    for row in data_table:
        if row.find('h3'):
            if 'Дата релиза' in row.find('h3'):
                row_realise_date = row.find('div', class_='pi-data-value').text.split('(')[0].strip()

    data_container = soup.find('span', id='Повышение_уровня_талантов').find_next('table').find('tbody').find_all('tr')[-1]

    talent_href = data_container.find_all('td')[2].find('a').get('href')
    weekly_boss_href = data_container.find_all('td')[3].find('a').get('href')


    talent_domain, row_talent_days = parse_talent_domain(talent_href)
    weekly_boss = parse_weekly_boss(weekly_boss_href)

    if name == 'Путешественник':
        row_talent_days = "Всегда"

    if 'Понедельник, четверг' in row_talent_days:
        talent_days = Days.MON_THU
    elif 'Вторник, пятница' in row_talent_days:
        talent_days = Days.TUE_FRI
    elif 'Среда, суббота' in row_talent_days:
        talent_days = Days.WED_SAT
    else:
        talent_days = Days.ALWAYS

    release_date = dateparser.parse(row_realise_date).replace(tzinfo=timezone.utc)

    character = Character(
        name=name.capitalize(),
        release_date=release_date,
        talent_days=talent_days,
        talent_domain=talent_domain,
        weekly_boss=weekly_boss
    )

    try:
        character.save()

    except Exception as e:
        print(f"Ошибка сохранения в базу: {e}")

def parse_talent_domain(href: str) -> tuple[str, str]:
    soup = parsing(href)

    data = soup.find_all('div', class_='pi-data-value')[-2]
    talent_domain, talent_days = data.text[:-1].split('(')

    return talent_domain.capitalize(), talent_days

def parse_weekly_boss(href: str) -> str:
    soup = parsing(href)

    data = soup.find_all('div', class_='pi-data-value')[-1]
    weekly_boss = data.find('span')

    if not weekly_boss:
        weekly_boss = data.find('a')

    return weekly_boss.text.strip().capitalize()

def parsing(href: str) -> BeautifulSoup:

    for attempt in range(5):
        try:
            url = href if 'http' in href else f'{base_url}{href}'
            print(url)
            response = requests.get(
                url=url,
                # headers={'User-Agent': ua},
                timeout=30
            )
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')

        except Exception as e:
            print(f"Попытка {attempt + 1}/5 не удалась: {e}")
            if attempt < 4:
                time.sleep(2)

    raise Exception('Request Timeout')
