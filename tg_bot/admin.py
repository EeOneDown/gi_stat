from django.contrib import admin

from tg_bot.models import Character, User, UserCharacter

admin.site.register(Character)
admin.site.register(User)
admin.site.register(UserCharacter)
