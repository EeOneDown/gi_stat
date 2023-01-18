from django.core.management.base import BaseCommand

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

        Character.objects.bulk_create(
            [
                Character(
                    name="Дэхья",
                    talent_days=Days.WED_SAT,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Мика",
                    talent_days=Days.WED_SAT,
                    talent_domain=forsaken_rift,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Аль-Хайтам",
                    talent_days=Days.TUE_FRI,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Яо Яо", talent_days=Days.TUE_FRI, talent_domain=steeple_of_ignorance, weekly_boss=scaramouche
                ),
                Character(
                    name="Странник",
                    talent_days=Days.WED_SAT,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Фарузан",
                    talent_days=Days.MON_THU,
                    talent_domain=steeple_of_ignorance,
                    weekly_boss=scaramouche,
                ),
                Character(
                    name="Лайла", talent_days=Days.TUE_FRI, talent_domain=steeple_of_ignorance, weekly_boss=scaramouche
                ),
                Character(
                    name="Нахида", talent_days=Days.TUE_FRI, talent_domain=steeple_of_ignorance, weekly_boss=scaramouche
                ),
                Character(
                    name="Кандакия", talent_days=Days.MON_THU, talent_domain=steeple_of_ignorance, weekly_boss=raiden
                ),
                Character(
                    name="Сайно", talent_days=Days.MON_THU, talent_domain=steeple_of_ignorance, weekly_boss=raiden
                ),
                Character(
                    name="Нилу", talent_days=Days.WED_SAT, talent_domain=steeple_of_ignorance, weekly_boss=raiden
                ),
                Character(
                    name="Дендро ГГ", talent_days=Days.ALWAYS, talent_domain=steeple_of_ignorance, weekly_boss=raiden
                ),
                Character(
                    name="Дори", talent_days=Days.TUE_FRI, talent_domain=steeple_of_ignorance, weekly_boss=azhdaha
                ),
                Character(
                    name="Коллеи", talent_days=Days.WED_SAT, talent_domain=steeple_of_ignorance, weekly_boss=raiden
                ),
                Character(
                    name="Тигнари", talent_days=Days.MON_THU, talent_domain=steeple_of_ignorance, weekly_boss=raiden
                ),
                Character(name="Хэйдзо", talent_days=Days.MON_THU, talent_domain=violet_court, weekly_boss=raiden),
                Character(name="Куки Синобу", talent_days=Days.TUE_FRI, talent_domain=violet_court, weekly_boss=raiden),
                Character(name="Е Лань", talent_days=Days.MON_THU, talent_domain=taishan_mansion, weekly_boss=azhdaha),
                Character(name="Сяо", talent_days=Days.MON_THU, talent_domain=taishan_mansion, weekly_boss=childe),
                Character(name="Сян Лин", talent_days=Days.TUE_FRI, talent_domain=taishan_mansion, weekly_boss=dvalin),
                Character(name="Райдэн", talent_days=Days.WED_SAT, talent_domain=violet_court, weekly_boss=la_signora),
                Character(name="Рэйзор", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Альбедо", talent_days=Days.WED_SAT, talent_domain=forsaken_rift, weekly_boss=childe),
                Character(name="Чжун Ли", talent_days=Days.WED_SAT, talent_domain=taishan_mansion, weekly_boss=childe),
                Character(name="Чун Юнь", talent_days=Days.TUE_FRI, talent_domain=taishan_mansion, weekly_boss=dvalin),
                Character(name="Диона", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=childe),
                Character(name="Дилюк", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Тарталья", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=childe),
                Character(name="Синь Янь", talent_days=Days.WED_SAT, talent_domain=taishan_mansion, weekly_boss=childe),
                Character(name="Ноэлль", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Син Цю", talent_days=Days.WED_SAT, talent_domain=taishan_mansion, weekly_boss=andrius),
                Character(name="Фишль", talent_days=Days.WED_SAT, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(name="Мона", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(name="Итто", talent_days=Days.TUE_FRI, talent_domain=violet_court, weekly_boss=la_signora),
                Character(name="Барбара", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(name="Ху Тао", talent_days=Days.TUE_FRI, talent_domain=taishan_mansion, weekly_boss=childe),
                Character(name="Розария", talent_days=Days.WED_SAT, talent_domain=forsaken_rift, weekly_boss=childe),
                Character(name="Аяка", talent_days=Days.TUE_FRI, talent_domain=violet_court, weekly_boss=azhdaha),
                Character(name="Аято", talent_days=Days.TUE_FRI, talent_domain=violet_court, weekly_boss=raiden),
                Character(name="Сахароза", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(
                    name="Шэнь Хэ", talent_days=Days.MON_THU, talent_domain=taishan_mansion, weekly_boss=la_signora
                ),
                Character(name="Гань Юй", talent_days=Days.TUE_FRI, talent_domain=taishan_mansion, weekly_boss=childe),
                Character(name="Джинн", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Беннет", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Кокоми", talent_days=Days.MON_THU, talent_domain=violet_court, weekly_boss=la_signora),
                Character(name="Янь Фэй", talent_days=Days.WED_SAT, talent_domain=taishan_mansion, weekly_boss=azhdaha),
                Character(name="Венти", talent_days=Days.WED_SAT, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(name="Кадзуха", talent_days=Days.TUE_FRI, talent_domain=taishan_mansion, weekly_boss=azhdaha),
                Character(name="Саю", talent_days=Days.WED_SAT, talent_domain=violet_court, weekly_boss=azhdaha),
                Character(name="ГГ", talent_days=Days.ALWAYS, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Анемо ГГ", talent_days=Days.ALWAYS, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Электро ГГ", talent_days=Days.ALWAYS, talent_domain=violet_court, weekly_boss=azhdaha),
                Character(name="Гео ГГ", talent_days=Days.ALWAYS, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Тома", talent_days=Days.MON_THU, talent_domain=violet_court, weekly_boss=la_signora),
                Character(name="Ёимия", talent_days=Days.MON_THU, talent_domain=violet_court, weekly_boss=azhdaha),
                Character(name="Эмбер", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Элой", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=la_signora),
                Character(name="Кли", talent_days=Days.MON_THU, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(name="Бэй Доу", talent_days=Days.WED_SAT, talent_domain=taishan_mansion, weekly_boss=dvalin),
                Character(name="Кэ Цин", talent_days=Days.MON_THU, talent_domain=taishan_mansion, weekly_boss=andrius),
                Character(name="Кэйа", talent_days=Days.WED_SAT, talent_domain=forsaken_rift, weekly_boss=andrius),
                Character(
                    name="Нин Гуан", talent_days=Days.MON_THU, talent_domain=taishan_mansion, weekly_boss=andrius
                ),
                Character(name="Яэ Мико", talent_days=Days.WED_SAT, talent_domain=violet_court, weekly_boss=raiden),
                Character(name="Эола", talent_days=Days.TUE_FRI, talent_domain=forsaken_rift, weekly_boss=azhdaha),
                Character(name="Горо", talent_days=Days.WED_SAT, talent_domain=violet_court, weekly_boss=la_signora),
                Character(
                    name="Юнь Цзинь", talent_days=Days.TUE_FRI, talent_domain=taishan_mansion, weekly_boss=la_signora
                ),
                Character(name="Сара", talent_days=Days.TUE_FRI, talent_domain=violet_court, weekly_boss=la_signora),
                Character(name="Лиза", talent_days=Days.WED_SAT, talent_domain=forsaken_rift, weekly_boss=dvalin),
                Character(name="Ци Ци", talent_days=Days.MON_THU, talent_domain=taishan_mansion, weekly_boss=andrius),
            ],
            ignore_conflicts=True,
        )
