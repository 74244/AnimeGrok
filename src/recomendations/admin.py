from django.contrib import admin

from src.recomendations.models import RecArticle

@admin.register(RecArticle)
class RecArticleAdmin(admin.ModelAdmin):
    list_display = ('article',  'user', 'text',)
