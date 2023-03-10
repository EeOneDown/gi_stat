# Generated by Django 4.1.4 on 2022-12-26 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=64, unique=True)),
                ("icon", models.CharField(max_length=24, blank=True)),
                (
                    "talent_days",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Всегда"),
                            (1, "Понедельник/Четверг"),
                            (2, "Вторник/Пятница"),
                            (3, "Среда/Суббота"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("chat_id", models.BigIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="WeeklyBoss",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32, unique=True)),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="weekly_bosses", to="tg_bot.region"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserCharacter",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("normal_attack", models.PositiveSmallIntegerField(default=0)),
                ("elemental_skill", models.PositiveSmallIntegerField(default=0)),
                ("elemental_burst", models.PositiveSmallIntegerField(default=0)),
                ("character", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tg_bot.character")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tg_bot.user")),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="characters",
            field=models.ManyToManyField(related_name="users", through="tg_bot.UserCharacter", to="tg_bot.character"),
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32, unique=True)),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="domains", to="tg_bot.region"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="character",
            name="talent_domain",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="characters_for_td", to="tg_bot.domain"
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="weekly_boss",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="characters_for_wb", to="tg_bot.weeklyboss"
            ),
        ),
    ]
