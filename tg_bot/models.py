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
    talent_days = models.PositiveSmallIntegerField(choices=Days.choices)
    talent_domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="characters_for_td")
    weekly_boss = models.ForeignKey(WeeklyBoss, on_delete=models.CASCADE, related_name="characters_for_wb")

    def __str__(self):
        return self.name


class User(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    characters = models.ManyToManyField(Character, related_name="users", through="UserCharacter")


class UserCharacter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    normal_attack = models.PositiveSmallIntegerField(default=0)
    elemental_skill = models.PositiveSmallIntegerField(default=0)
    elemental_burst = models.PositiveSmallIntegerField(default=0)
