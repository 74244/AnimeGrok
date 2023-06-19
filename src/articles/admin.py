from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from mptt.admin import DraggableMPTTAdmin
from src.articles.models import (Category, Actor, Genre, Viewer, Article, 
                                 ArticleShot, RatingStar, Rating, Review, Video)

class ArticleAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""

    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    search_help_text = 'Поиск по названию'
    save_as = True
    save_on_top = True

@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ('user', 'description', 'age', 'image')
    save_as = True
    save_on_top = True

@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'description',)
    # list_editable = ('name_en')
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
class ArticleAdmin(TranslationAdmin):
    list_display = ('title', 'title_alt', 'date_aired',  'activity', 'series', 'season',
                    'user', 'on_main', 'get_poster_in_list',)
    list_display_links = ('title',)
    prepopulated_fields = {'link': ('title_alt',)}
    search_fields = ('title',)
    save_as = True
    save_on_top = True
    readonly_fields = ('get_poster_in_article',)
    form = ArticleAdminForm
    # ordering = ('id',)
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
            'fields':(('author', 'studio', 'country'), ('type','quality') ),
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
        (None, {
            'fields':('videos',)
        }),
    )

    def get_views(self, obj):
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
    get_views.short_description = "Просмотры"
    get_poster_in_list.short_description = "Изображение"
    get_poster_in_article.short_description = "Изображение"

@admin.register(Review)
class ReviewAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'create_at')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('create_at',)

@admin.register(ArticleShot)
class ArticleShotAdmin(TranslationAdmin):
    list_display = ('article', 'title', 'description', 'image')
    save_as = True
    save_on_top = True

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('article', 'star')
    
@admin.register(Video)
class VideoAdmin(TranslationAdmin):
    list_display = ('article', 'episode', 'title',  'create_at', 'file')
    list_editable = ('episode', 'file')
    search_fields = ('article',)
    save_as = True
    ordering = ('-create_at',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields':('article',),
        }),
        (None, {
            'fields':(('episode', 'title'),),
        }),
        (None, {
            'fields':('file', 'image'),
        }),
    )

admin.site.register(RatingStar)

