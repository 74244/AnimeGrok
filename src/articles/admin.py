from django.contrib import admin
from src.articles.models import Category, Actor, Genre, Ip, Article, ArticleShot, RatingStar, Rating, Reviews

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'link': ('title_alt',)}


admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Ip)
admin.site.register(ArticleShot)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Reviews)