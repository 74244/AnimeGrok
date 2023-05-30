from django.contrib import admin

from src.recomendations.models import RecArticle

@admin.register(RecArticle)
class RecArticleAdmin(admin.ModelAdmin):
    list_display = ('article', 'text', 'get_users_count')

    def get_users_count(self, obj):
        return obj.users.count()