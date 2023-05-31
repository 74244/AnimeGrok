from modeltranslation.translator import register, TranslationOptions
from src.articles.models import Category, Actor, Genre, Article, Review, Video

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('user', 'description')

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'country', 'season')

