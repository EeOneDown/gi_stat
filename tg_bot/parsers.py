import time
import dateparser

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from tg_bot.models import Character


ua = UserAgent().random


def get_characters_list() -> list:
    characters = Character
    characters_list = list(characters.objects.order_by("release_date").all())

    return characters_list

def save_data(character_list: dict[str, str]):
    print(character_list)
    if all(character_list.values()):
        Character.objects.create(
            name=character_list['name'],
            release_date=character_list['release_date'],
            talent_days=character_list['talent_days'],
            talent_domain=character_list['talent_domain'],
            weekly_boss=character_list['weekly_boss']
        )

    else:
        raise Exception('Invalid character name')

def sync_characters() -> None:

    result = {}

    soup = parsing('/ru/wiki/%D0%9F%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%B6%D0%B8')

    characters_temp = soup.find('table', class_='article-table').find('tbody').find_all('tr')
    for character in characters_temp[1:]:
        char_stats = character.find_all('td')[1].find('a')
        result[char_stats.get('title')] = char_stats.get('href')

    characters_list = get_characters_list()

    for char in result.keys():
        if char not in characters_list:
            add_new_character(char, f'{result[char]}')

def add_new_character(name: str, href: str) -> None:
    soup = parsing(href)

    data_table = soup.find_all('div', class_='pi-item')
    for row in data_table:
        if row.find('h3'):
            if 'Дата релиза' in row.find('h3'):
                row_realise_date = row.find('div', class_='pi-data-value').text.split('(')[0].strip()

    data_container = soup.find('span', id='Повышение_уровня_талантов').find_next('table').find('tbody').find_all('tr')[-1]

    talent_href = data_container.find_all('td')[2].find('a').get('href')
    weekly_boos_href = data_container.find_all('td')[3].find('a').get('href')


    talent_domain, row_talent_days = parse_talent_domain(talent_href)
    weekly_boss = parse_weekly_boss(weekly_boos_href)

    if 'Понедельник, четверг' in row_talent_days:
        talent_days = 1
    elif 'Вторник, пятница' in row_talent_days:
        talent_days = 2
    elif 'Среда, суббота' in row_talent_days:
        talent_days = 3
    else:
        talent_days = 0

    realise_date = dateparser.parse(row_realise_date)

    character_data = {
        'name': name,
        'release_date': realise_date,
        'talent_days': talent_days,
        'talent_domain': talent_domain,
        'weekly_boss': weekly_boss,
    }

    save_data(character_data)



def parse_talent_domain(href: str) -> (str, str):
    soup = parsing(href)

    data = soup.find_all('div', class_='pi-data-value')[-2]
    talent_domain, talent_days = data.text[:-1].split('(')

    return talent_domain, talent_days

def parse_weekly_boss(href: str) -> str:
    soup = parsing(href)

    data = soup.find_all('div', class_='pi-data-value')[-1]
    weekly_boss = data.find('span')

    if not weekly_boss:
        weekly_boss = data.find('a')

    return weekly_boss.text.strip()

def parsing(href: str) -> BeautifulSoup:
    base_url = 'https://genshin-impact.fandom.com'

    for attempt in range(5):
        try:
            url = href if 'http' in href else f'{base_url}{href}'
            print(url)
            response = requests.get(
                url=url,
                headers={'User-Agent': ua},
                timeout=30
            )
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')

        except Exception as e:
            print(f"Попытка {attempt + 1}/5 не удалась: {e}")
            if attempt < 4:
                time.sleep(2)

    raise Exception('Request Timeout')
