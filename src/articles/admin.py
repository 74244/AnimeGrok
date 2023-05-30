from django.contrib import admin
from django.utils.safestring import mark_safe

from mptt.admin import DraggableMPTTAdmin
from src.articles.models import (Category, Actor, Genre, Viewer, Article, 
                                 ArticleShot, RatingStar, Rating, Review, Video)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    search_help_text = 'Поиск по названию'
    save_as = True
    save_on_top = True

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'age', 'image')
    # search_fields = ('user',)             #FIXME:Исправить поиск
    # search_help_text = 'Поиск по никнейму'
    save_as = True
    save_on_top = True

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    search_help_text = 'Поиск по названию'
    save_as = True
    save_on_top = True

@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user', 'viewed_on')
    search_fields = ('viewed_on',)
    search_help_text = 'Поиск по дате просмотра'
    save_as = True
    save_on_top = True


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_alt', 'date_aired',  'activity', 'series', 'season', 
                    'get_reviews_count', 'get_viewers_count','user', 'on_main', 'get_poster_in_list',)
    prepopulated_fields = {'link': ('title_alt',)}
    search_fields = ('title',)
    save_as = True
    save_on_top = True
    readonly_fields = ('get_poster_in_article',)
    fieldsets = (
        (None, {
            'fields':('on_main',),
        }),
        (None, {
            'fields':('get_poster_in_article', 'poster'),
        }),
        (None, {
            'fields':('category', ),
        }),
        (None, {
            'fields':(('title', 'title_alt'),),
        }),
        (None, {
            'fields':('description',),
        }),
        (None, {
            'fields':('genres',),
        }),
        (None, {
            'fields':(('author', 'studio', 'coutry'), ('type','quality') ),
        }),
        (None, {
            'fields':(('activity', 'series'), 'date_aired'),
        }),
        (None, {
            'fields':(('voicing', 'timing', 'subtitles'),),
        }),
        (None, {
            'fields':('season',),
        }),
        (None, {
            'fields':('link',)
        }),
    )

    def get_viewers_count(self, obj):
        pass
        # return obj.viewers.count()

    def get_reviews_count(self, obj):
        pass
        # return obj.reviews.count()

    def get_poster_in_list(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

    def get_poster_in_article(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="120" height="150"')

    get_reviews_count.short_description = "Отзывы"
    get_viewers_count.short_description = "Просмотры"
    get_poster_in_list.short_description = "Изображение"
    get_poster_in_article.short_description = "Изображение"

@admin.register(Review)
class ReviewAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'create_at')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('create_at',)

@admin.register(ArticleShot)
class ArticleShotAdmin(admin.ModelAdmin):
    list_display = ('article', 'title', 'description', 'image')
    save_as = True
    save_on_top = True

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('article', 'star')
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('article', 'episode', 'title',  'create_at')
    search_fields = ('article',)
    save_as = True
    save_on_top = True
    fieldsets = (
        (None, {
            'fields':(('article', 'episode', 'title'),),
        }),
        (None, {
            'fields':('file', 'image'),
        }),
    )

admin.site.register(RatingStar)

