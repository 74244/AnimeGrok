from modeltranslation.translator import register, TranslationOptions
from src.articles.models import Category, Actor, Genre, Article, Video, ArticleShot

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('description',)

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'author', 'type', 'studio', 'activity', 'duration', 'country', 'season')

@register(ArticleShot)
class ArticleShotTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title',)