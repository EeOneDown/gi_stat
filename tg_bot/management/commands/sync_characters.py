from django.core.management.base import BaseCommand
from tg_bot.parsers import sync_characters


class Command(BaseCommand):
    def handle(self, *args, **options):
        sync_characters()