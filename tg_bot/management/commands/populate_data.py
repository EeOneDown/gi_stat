from django.core.management.base import BaseCommand
from django.utils import timezone

from tg_bot.models import Region, Domain, WeeklyBoss, Character, Days


class Command(BaseCommand):
    def handle(self, *args, **options):
        mondstadt = Region.objects.create(name="Мондштадт")
        liyue = Region.objects.create(name="Ли Юэ")
        inazuma = Region.objects.create(name="Инадзума")
        sumeru = Region.objects.create(name="Сумеру")
        Region.objects.create(name="Фонтейн")  # fontaine
        Region.objects.create(name="Натлан")  # natlan
        Region.objects.create(name="Снежная")  # snezhnaya

        forsaken_rift = Domain.objects.create(name="Забытый каньон", region=mondstadt)
        taishan_mansion = Domain.objects.create(name="Тайшаньфу", region=liyue)
        violet_court = Domain.objects.create(name="Фиалковый зал", region=inazuma)
        steeple_of_ignorance = Domain.objects.create(name="Башня невежества", region=sumeru)

        andrius = WeeklyBoss.objects.create(name="Андриус", region=mondstadt)
        dvalin = WeeklyBoss.objects.create(name="Двалин", region=mondstadt)
        childe = WeeklyBoss.objects.create(name="Чайльд", region=liyue)
        azhdaha = WeeklyBoss.objects.create(name="Аждаха", region=liyue)
        la_signora = WeeklyBoss.objects.create(name="Синьора", region=inazuma)
        raiden = WeeklyBoss.objects.create(name="Райден", region=inazuma)
        scaramouche = WeeklyBoss.objects.create(name="Скарамучча", region=sumeru)

        tz = timezone.get_current_timezone()
        Character.objects.bulk_create(
            [
                # announced
                Character(
                    name="Дэхья",
                    release_date=timezone.datetime(2025, 9, 28, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Мика",
                    release_date=timezone.datetime(2025, 9, 28, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=scaramouche,
                ),
                # released
                Character(
                    name="Аль-Хайтам",
                    release_date=timezone.datetime(2023, 1, 18, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Яо Яо",
                    release_date=timezone.datetime(2023, 1, 18, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Странник",
                    release_date=timezone.datetime(2022, 12, 7, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Фарузан",
                    release_date=timezone.datetime(2022, 12, 7, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Лайла",
                    release_date=timezone.datetime(2022, 11, 18, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Нахида",
                    release_date=timezone.datetime(2022, 11, 2, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Нилу",
                    release_date=timezone.datetime(2022, 10, 14, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Сайно",
                    release_date=timezone.datetime(2022, 9, 28, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Кандакия",
                    release_date=timezone.datetime(2022, 9, 28, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Дори",
                    release_date=timezone.datetime(2022, 9, 9, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Тигнари",
                    release_date=timezone.datetime(2022, 8, 24, 0, 0, 2, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Коллеи",
                    release_date=timezone.datetime(2022, 8, 24, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Дендро ГГ",
                    release_date=timezone.datetime(2022, 8, 24, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.ALWAYS,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Хэйдзо",
                    release_date=timezone.datetime(2022, 7, 13, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=violet_court,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Куки Синобу",
                    release_date=timezone.datetime(2022, 6, 21, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=violet_court,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Е Лань",
                    release_date=timezone.datetime(2022, 5, 31, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=taishan_mansion,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Аято",
                    release_date=timezone.datetime(2022, 3, 30, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=violet_court,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Яэ Мико",
                    release_date=timezone.datetime(2022, 2, 16, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=violet_court,
                    weekly_boss=raiden,
                ),
                Character(
                    name="Шэнь Хэ",
                    release_date=timezone.datetime(2022, 1, 5, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=taishan_mansion,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Юнь Цзинь",
                    release_date=timezone.datetime(2022, 1, 5, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=taishan_mansion,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Итто",
                    release_date=timezone.datetime(2021, 12, 14, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=violet_court,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Горо",
                    release_date=timezone.datetime(2021, 12, 14, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=violet_court,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Тома",
                    release_date=timezone.datetime(2021, 11, 2, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=violet_court,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Кокоми",
                    release_date=timezone.datetime(2021, 9, 21, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=violet_court,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Райдэн",
                    release_date=timezone.datetime(2021, 9, 1, 0, 0, 2, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=violet_court,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Сара",
                    release_date=timezone.datetime(2021, 9, 1, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=violet_court,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Элой",
                    release_date=timezone.datetime(2021, 9, 1, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=la_signora,
                ),
                Character(
                    name="Ёимия",
                    release_date=timezone.datetime(2021, 8, 10, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=violet_court,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Саю",
                    release_date=timezone.datetime(2021, 8, 10, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=violet_court,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Аяка",
                    release_date=timezone.datetime(2021, 7, 21, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=violet_court,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Электро ГГ",
                    release_date=timezone.datetime(2021, 7, 21, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.ALWAYS,
                    talent_domain=violet_court,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Кадзуха",
                    release_date=timezone.datetime(2021, 6, 29, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=taishan_mansion,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Эола",
                    release_date=timezone.datetime(2021, 5, 18, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Янь Фэй",
                    release_date=timezone.datetime(2021, 4, 28, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=taishan_mansion,
                    weekly_boss=azhdaha,
                ),
                Character(
                    name="Розария",
                    release_date=timezone.datetime(2021, 4, 6, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=childe,
                ),
                Character(
                    name="Ху Тао",
                    release_date=timezone.datetime(2021, 3, 2, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=taishan_mansion,
                    weekly_boss=childe,
                ),
                Character(
                    name="Сяо",
                    release_date=timezone.datetime(2021, 2, 3, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=taishan_mansion,
                    weekly_boss=childe,
                ),
                Character(
                    name="Гань Юй",
                    release_date=timezone.datetime(2021, 1, 12, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=taishan_mansion,
                    weekly_boss=childe,
                ),
                Character(
                    name="Альбедо",
                    release_date=timezone.datetime(2020, 12, 23, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=childe,
                ),
                Character(
                    name="Чжун Ли",
                    release_date=timezone.datetime(2020, 12, 1, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=taishan_mansion,
                    weekly_boss=childe,
                ),
                Character(
                    name="Синь Янь",
                    release_date=timezone.datetime(2020, 12, 1, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=taishan_mansion,
                    weekly_boss=childe,
                ),
                Character(
                    name="Тарталья",
                    release_date=timezone.datetime(2020, 11, 11, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=childe,
                ),
                Character(
                    name="Диона",
                    release_date=timezone.datetime(2020, 11, 11, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=childe,
                ),
                Character(
                    name="Кли",
                    release_date=timezone.datetime(2020, 10, 20, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Венти",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 22, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Кэ Цин",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 21, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=taishan_mansion,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Мона",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 20, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Ци Ци",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 19, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=taishan_mansion,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Дилюк",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 18, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Джинн",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 17, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Сахароза",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 16, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Чун Юнь",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 15, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=taishan_mansion,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Ноэлль",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 14, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Беннет",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 13, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Фишль",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 12, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Нин Гуан",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 11, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=taishan_mansion,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Син Цю",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 10, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=taishan_mansion,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Бэй Доу",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 9, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=taishan_mansion,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Сян Лин",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 8, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=taishan_mansion,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Рэйзор",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 7, tzinfo=tz),
                    talent_days=Days.TUE_FRI,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Барбара",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 6, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Лиза",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 5, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Кэйа",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 4, tzinfo=tz),
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=andrius,
                ),
                Character(
                    name="Эмбер",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 3, tzinfo=tz),
                    talent_days=Days.MON_THU,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Гео ГГ",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 2, tzinfo=tz),
                    talent_days=Days.ALWAYS,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="Анемо ГГ",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 1, tzinfo=tz),
                    talent_days=Days.ALWAYS,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
                Character(
                    name="ГГ",
                    release_date=timezone.datetime(2020, 9, 28, 0, 0, 0, tzinfo=tz),
                    talent_days=Days.ALWAYS,
                    talent_domain=forsaken_rift,
                    weekly_boss=dvalin,
                ),
            ],
            ignore_conflicts=True,
        )
