from accounts.models import Team
from django.contrib import admin

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'resolved')

admin.site.register(Team, TeamAdmin)
