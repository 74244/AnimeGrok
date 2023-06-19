from collections import OrderedDict
from datetime import datetime, timedelta

from django import template
from django.conf.global_settings import LANGUAGE_CODE
from django.core.cache import cache
from django.db.models import Count, Max
from django.utils.translation import get_language

from src.recomendations.models import RecArticle
from src.articles.models import Review, Article, Video

register = template.Library()

@register.simple_tag()
def get_home_slider_articles():
    """Список аниме на главную для слайдера"""

    home_slider_cache_name = 'home_slider_cache'
    home_slider_cache = cache.get(home_slider_cache_name)
    if home_slider_cache:
        result = home_slider_cache
    else:
        result = Article.objects.filter(on_main=True).only('title', 'link', 'genres','poster').prefetch_related('genres')
        cache.set(home_slider_cache_name, result, 60  * 60)
    return result


#TODO: Исправить фильтрацию данных на по квартальную или т.п.
@register.simple_tag()
def get_season_articles(quantity):
    """ Вывод аниме по сезону """

    season_articles_cache_name = 'season_articles_cache'
    season_articles_cache = cache.get(season_articles_cache_name)
    if season_articles_cache:
        result = season_articles_cache
    else:
        result = Article.objects.prefetch_related('viewers', 'genres', 'article_episodes').filter(season__contains='2023-Весна').only('title', 'link', 'genres', 'viewers', 'season', 'series', 'poster')[:quantity]
        cache.set(season_articles_cache_name, result, 60  * 60)

    return result

@register.simple_tag()
def get_last_articles(quantity):
    """Вывод последних добавленных аниме"""

    last_articles_cache_name = 'last_articles_cache'
    last_articles_cache = cache.get(last_articles_cache_name)
    if last_articles_cache:
        result = last_articles_cache
    else:
        data = Video.objects.values_list('article_id', flat=True).order_by('-create_at')
        res = list(OrderedDict.fromkeys(data))
        result = Article.objects.prefetch_related('viewers', 'genres', 'article_episodes').filter(pk__in=res).only('title', 'link', 'genres', 'viewers', 'season', 'series', 'poster')[:quantity]
        cache.set(last_articles_cache_name, result, 60  * 60)

    return result


@register.inclusion_tag('articles/list_top_views.html')
def get_top_views_articles(quantity):
    """Вывод аниме с наибольшими просмотрами """

    top_v_articles_cache_name = 'top_v_articles_cache'
    top_v_articles_cache = cache.get(top_v_articles_cache_name)
    if top_v_articles_cache:
        result = top_v_articles_cache
    else:
        result = Article.objects.annotate(top_views=Count('viewers')).order_by('-top_views')[:quantity].prefetch_related('viewers', 'article_episodes').only('title', 'link', 'viewers', 'series', 'poster', 'date_aired')
        cache.set(top_v_articles_cache_name, result, 60  * 60)
    return {'top_v_articles': result}


@register.inclusion_tag('articles/recommended_articles.html')
def get_recommended_articles(quantity):
    """Вывод аниме из топа рекомендаций"""

    recommended_articles_cache_name = 'recommended_articles_cache'
    recommended_articles_cache = cache.get(recommended_articles_cache_name)
    if recommended_articles_cache:
        result = recommended_articles_cache
    else:
        result = Article.objects.prefetch_related('genres', 'viewers', 'article_episodes').exclude(article_recs__isnull=True).only('title', 'link', 'genres', 'viewers', 'season', 'series', 'poster')
        cache.set(recommended_articles_cache_name, result, 60  * 60)
    return {'r_articles': result}

@register.simple_tag()
def get_dorams(quantity):
    """Вывод дорам"""
    
    dorams_cache_name = 'dorams_cache'
    dorams_cache = cache.get(dorams_cache_name)
    if dorams_cache:
        result = dorams_cache
    else:
        result = Article.objects.prefetch_related('viewers', 'genres', 'article_episodes').filter(category__link='dorama').only('title', 'link', 'viewers', 'series', 'poster')[:quantity]
        cache.set(dorams_cache_name, result, 60  * 60)

    return result


@register.inclusion_tag('articles/list_new_reviews.html')
def get_last_reviews():
    """Вывод последних комментариев на странице со списком аниме"""

    last_reviews = Review.objects.select_related('article').order_by('-create_at').only('article', 'article__id', 'article__genres__name', 'article__poster', 'article__link', 'article__viewers').prefetch_related('article__genres', 'article__viewers')[:4]
    return {'last_reviews': last_reviews}

    