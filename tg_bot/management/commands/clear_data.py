from django.core.management.base import BaseCommand

from tg_bot.models import Region, Domain, WeeklyBoss, Character


class Command(BaseCommand):
    def handle(self, *args, **options):
        Region.objects.all().delete()
        Domain.objects.all().delete()
        WeeklyBoss.objects.all().delete()
        Character.objects.all().delete()
