from django.contrib import admin
from src.articles.models import Category, Actor, Genre, Viewer, Article, ArticleShot, RatingStar, Rating, Review, Video

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', )
    prepopulated_fields = {'link': ('title_alt',)}

@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user')

admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(ArticleShot)
admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Video)