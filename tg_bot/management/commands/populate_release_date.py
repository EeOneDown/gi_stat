from django.core.management.base import BaseCommand
from django.utils import timezone

from tg_bot.models import Character


class Command(BaseCommand):
    def handle(self, *args, **options):
        tz = timezone.get_current_timezone()

        # announced
        Character.objects.filter(name="Дэхья").update(
            release_date=timezone.datetime(2025, 9, 28, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Мика").update(
            release_date=timezone.datetime(2025, 9, 28, 0, 0, 0, tzinfo=tz),
        )
        # released
        Character.objects.filter(name="Аль-Хайтам").update(
            release_date=timezone.datetime(2023, 1, 18, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Яо Яо").update(
            release_date=timezone.datetime(2023, 1, 18, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Странник").update(
            release_date=timezone.datetime(2022, 12, 7, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Фарузан").update(
            release_date=timezone.datetime(2022, 12, 7, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Лайла").update(
            release_date=timezone.datetime(2022, 11, 18, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Нахида").update(
            release_date=timezone.datetime(2022, 11, 2, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Нилу").update(
            release_date=timezone.datetime(2022, 10, 14, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Сайно").update(
            release_date=timezone.datetime(2022, 9, 28, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Кандакия").update(
            release_date=timezone.datetime(2022, 9, 28, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Дори").update(
            release_date=timezone.datetime(2022, 9, 9, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Тигнари").update(
            release_date=timezone.datetime(2022, 8, 24, 0, 0, 2, tzinfo=tz),
        )
        Character.objects.filter(name="Коллеи").update(
            release_date=timezone.datetime(2022, 8, 24, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Дендро ГГ").update(
            release_date=timezone.datetime(2022, 8, 24, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Хэйдзо").update(
            release_date=timezone.datetime(2022, 7, 13, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Куки Синобу").update(
            release_date=timezone.datetime(2022, 6, 21, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Е Лань").update(
            release_date=timezone.datetime(2022, 5, 31, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Аято").update(
            release_date=timezone.datetime(2022, 3, 30, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Яэ Мико").update(
            release_date=timezone.datetime(2022, 2, 16, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Шэнь Хэ").update(
            release_date=timezone.datetime(2022, 1, 5, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Юнь Цзинь").update(
            release_date=timezone.datetime(2022, 1, 5, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Итто").update(
            release_date=timezone.datetime(2021, 12, 14, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Горо").update(
            release_date=timezone.datetime(2021, 12, 14, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Тома").update(
            release_date=timezone.datetime(2021, 11, 2, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Кокоми").update(
            release_date=timezone.datetime(2021, 9, 21, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Райдэн").update(
            release_date=timezone.datetime(2021, 9, 1, 0, 0, 2, tzinfo=tz),
        )
        Character.objects.filter(name="Сара").update(
            release_date=timezone.datetime(2021, 9, 1, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Элой").update(
            release_date=timezone.datetime(2021, 9, 1, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Ёимия").update(
            release_date=timezone.datetime(2021, 8, 10, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Саю").update(
            release_date=timezone.datetime(2021, 8, 10, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Аяка").update(
            release_date=timezone.datetime(2021, 7, 21, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Электро ГГ").update(
            release_date=timezone.datetime(2021, 7, 21, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Кадзуха").update(
            release_date=timezone.datetime(2021, 6, 29, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Эола").update(
            release_date=timezone.datetime(2021, 5, 18, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Янь Фэй").update(
            release_date=timezone.datetime(2021, 4, 28, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Розария").update(
            release_date=timezone.datetime(2021, 4, 6, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Ху Тао").update(
            release_date=timezone.datetime(2021, 3, 2, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Сяо").update(
            release_date=timezone.datetime(2021, 2, 3, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Гань Юй").update(
            release_date=timezone.datetime(2021, 1, 12, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Альбедо").update(
            release_date=timezone.datetime(2020, 12, 23, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Чжун Ли").update(
            release_date=timezone.datetime(2020, 12, 1, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Синь Янь").update(
            release_date=timezone.datetime(2020, 12, 1, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Тарталья").update(
            release_date=timezone.datetime(2020, 11, 11, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="Диона").update(
            release_date=timezone.datetime(2020, 11, 11, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Кли").update(
            release_date=timezone.datetime(2020, 10, 20, 0, 0, 0, tzinfo=tz),
        )
        Character.objects.filter(name="Венти").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 22, tzinfo=tz),
        )
        Character.objects.filter(name="Кэ Цин").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 21, tzinfo=tz),
        )
        Character.objects.filter(name="Мона").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 20, tzinfo=tz),
        )
        Character.objects.filter(name="Ци Ци").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 19, tzinfo=tz),
        )
        Character.objects.filter(name="Дилюк").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 18, tzinfo=tz),
        )
        Character.objects.filter(name="Джинн").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 17, tzinfo=tz),
        )
        Character.objects.filter(name="Сахароза").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 16, tzinfo=tz),
        )
        Character.objects.filter(name="Чун Юнь").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 15, tzinfo=tz),
        )
        Character.objects.filter(name="Ноэлль").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 14, tzinfo=tz),
        )
        Character.objects.filter(name="Беннет").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 13, tzinfo=tz),
        )
        Character.objects.filter(name="Фишль").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 12, tzinfo=tz),
        )
        Character.objects.filter(name="Нин Гуан").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 11, tzinfo=tz),
        )
        Character.objects.filter(name="Син Цю").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 10, tzinfo=tz),
        )
        Character.objects.filter(name="Бэй Доу").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 9, tzinfo=tz),
        )
        Character.objects.filter(name="Сян Лин").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 8, tzinfo=tz),
        )
        Character.objects.filter(name="Рэйзор").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 7, tzinfo=tz),
        )
        Character.objects.filter(name="Барбара").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 6, tzinfo=tz),
        )
        Character.objects.filter(name="Лиза").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 5, tzinfo=tz),
        )
        Character.objects.filter(name="Кэйа").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 4, tzinfo=tz),
        )
        Character.objects.filter(name="Эмбер").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 3, tzinfo=tz),
        )
        Character.objects.filter(name="Гео ГГ").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 2, tzinfo=tz),
        )
        Character.objects.filter(name="Анемо ГГ").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 1, tzinfo=tz),
        )
        Character.objects.filter(name="ГГ").update(
            release_date=timezone.datetime(2020, 9, 28, 0, 0, 0, tzinfo=tz),
        )
