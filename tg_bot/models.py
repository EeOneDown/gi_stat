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


class Region(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=32, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="domains")

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class WeeklyBoss(models.Model):
    name = models.CharField(max_length=32, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="weekly_bosses")

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=64, unique=True)
    icon = models.CharField(max_length=24, blank=True)
    release_date = models.DateTimeField(null=True)
    talent_days = models.PositiveSmallIntegerField(choices=Days.choices)
    talent_domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="characters_for_td")
    weekly_boss = models.ForeignKey(WeeklyBoss, on_delete=models.CASCADE, related_name="characters_for_wb")

    class Meta:
        ordering = ["-release_date"]

    def __str__(self):
        return self.name

    @classmethod
    def get_for_today(cls, days: list[int]) -> list["Character"]:
        return list(
            cls.objects.filter(talent_days__in=days)
            .select_related("talent_domain__region")
            .order_by("talent_domain__region_id")
            .all()
        )

    @classmethod
    def get_for_week(cls) -> list["Character"]:
        return list(
            cls.objects.select_related("talent_domain__region")
            .order_by("talent_days", "talent_domain__region_id")
            .all()
        )

    @classmethod
    def get_for_weekly_bosses(cls) -> list["Character"]:
        return list(cls.objects.select_related("weekly_boss").order_by("weekly_boss_id").all())


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
    def get_for_today(cls, chat_id: int, days: list[int]) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__chat_id=chat_id, character__talent_days__in=days)
            .select_related("character__talent_domain__region")
            .order_by("character__talent_domain__region_id")
            .all()
        )

    @classmethod
    def get_for_week(cls, chat_id: int) -> list["UserCharacter"]:
        return list(
            UserCharacter.objects.filter(user__chat_id=chat_id)
            .select_related("character__talent_domain__region")
            .order_by("character__talent_days", "character__talent_domain__region_id")
            .all()
        )

    @classmethod
    def get_for_weekly_bosses(cls, chat_id: int) -> list["UserCharacter"]:
        return list(
            UserCharacter.objects.filter(user__chat_id=chat_id)
            .select_related("character__weekly_boss")
            .order_by("character__weekly_boss_id")
            .all()
        )

    @classmethod
    def get_for_daily_dispatch(cls, days: list[int]) -> list["UserCharacter"]:
        return list(
            cls.objects.filter(user__is_subscribed=True, character__talent_days__in=days)
            .select_related("user", "character__talent_domain__region")
            # order by region for in-code 'group by'
            .order_by("user_id", "character__talent_domain__region_id")
            .all()
        )
