from django.db import models


class Days(models.IntegerChoices):
    ALWAYS = 0, "Всегда"
    MON_THU = 1, "Понедельник/Четверг"
    TUE_FRI = 2, "Вторник/Пятница"
    WED_SAT = 3, "Среда/Суббота"

    @classmethod
    def get_by_weekday(cls, weekday: int) -> list[int]:
        days = [cls.MON_THU, cls.TUE_FRI, cls.WED_SAT, cls.ALWAYS]
        if weekday == 6:
            return days
        return [days[weekday % 3], cls.ALWAYS]


class Character(models.Model):
    name = models.TextField(unique=True)
    release_date = models.DateTimeField()
    talent_days = models.PositiveSmallIntegerField(choices=Days.choices)
    talent_domain = models.TextField()
    weekly_boss = models.TextField()

    def __str__(self):
        return self.name

    @classmethod
    def get_for_follow_characters(cls, chat_id: int) -> list["Character"]:
        return list(cls.objects.exclude(users__chat_id=chat_id).order_by("-release_date").all())

    @classmethod
    def get_for_unfollow_characters(cls, chat_id: int) -> list["Character"]:
        return list(cls.objects.filter(users__chat_id=chat_id).order_by("-release_date").all())

    @classmethod
    def get_for_today(cls, days: list[int]) -> list["Character"]:
        return list(cls.objects.filter(talent_days__in=days).order_by("talent_domain", "-release_date").all())

    @classmethod
    def get_for_week(cls) -> list["Character"]:
        return list(
            cls.objects.select_related()
            .order_by("talent_days", "talent_domain", "-release_date")
            .all()
        )

    @classmethod
    def get_for_weekly_bosses(cls) -> list["Character"]:
        return list(cls.objects.order_by("weekly_boss", "-release_date").all())


class User(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    characters = models.ManyToManyField(Character, related_name="users", through="UserCharacter")
    is_subscribed = models.BooleanField(default=False)


class UserCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    normal_attack = models.PositiveSmallIntegerField(default=0)
    elemental_skill = models.PositiveSmallIntegerField(default=0)
    elemental_burst = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def get_for_character_list(cls, chat_id: int) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__chat_id=chat_id)
            .select_related("character")
            .order_by("character__name")
            .all()
        )

    @classmethod
    def get_for_today(cls, chat_id: int, days: list[int]) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__chat_id=chat_id, character__talent_days__in=days)
            .select_related("character")
            .order_by("character__talent_domain", "-character__release_date")
            .all()
        )

    @classmethod
    def get_for_week(cls, chat_id: int) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__chat_id=chat_id)
            .select_related("character")
            .order_by("character__talent_days", "character__talent_domain", "-character__release_date")
            .all()
        )

    @classmethod
    def get_for_weekly_bosses(cls, chat_id: int) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__chat_id=chat_id)
            .select_related("character")
            .order_by("character__weekly_boss", "-character__release_date")
            .all()
        )

    @classmethod
    def get_for_daily_dispatch(cls, days: list[int]) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__is_subscribed=True, character__talent_days__in=days)
            .select_related("user", "character")
            .order_by("user_id", "character__talent_domain", "-character__release_date")
            .all()
        )
