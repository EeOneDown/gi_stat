# Generated by Django 4.1.4 on 2022-12-29 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tg_bot", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_subscribed",
            field=models.BooleanField(default=False),
        ),
    ]
