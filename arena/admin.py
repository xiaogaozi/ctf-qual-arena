from arena.models import Question
from django.contrib import admin

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'score', 'desc', 'status', 'resolved_teams')

admin.site.register(Question, QuestionAdmin)
