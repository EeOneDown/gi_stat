from django.contrib import admin

from tg_bot.models import Region, Domain, WeeklyBoss, Character, User, UserCharacter

admin.site.register(Region)
admin.site.register(Domain)
admin.site.register(WeeklyBoss)
admin.site.register(Character)
admin.site.register(User)
admin.site.register(UserCharacter)
