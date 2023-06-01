from collections import OrderedDict
from datetime import datetime, timedelta

from django import template
from django.db.models import Count

from src.recomendations.models import RecArticle
from src.articles.models import Review, Article, Video
register = template.Library()




@register.inclusion_tag('articles/home_slider_articles.html')
def get_home_slider_articles():
    home_slider_articles = Article.objects.filter(on_main=True)
    return {'home_slider_articles': home_slider_articles}


#TODO: Исправить фильтрацию данных на по квартальную или т.п.
@register.simple_tag()
def get_season_articles(quantity):
    """ Вывод аниме по сезону """

    return Article.objects.filter(season__contains='2023-Весна')[:quantity]

@register.simple_tag()
def get_last_articles(quantity):
    """Вывод последних добавленных аниме"""
    
    data = Video.objects.order_by('-episode').values_list('article_id', flat=True)
    res = list(OrderedDict.fromkeys(data))
    last_articles = Article.objects.filter(pk__in=res)[:quantity]
    return last_articles


@register.inclusion_tag('articles/list_top_views.html')
def get_top_views_articles(quantity):
    """Вывод аниме с наибольшими просмотрами """
    top_v_articles = Article.objects.annotate(top_views=Count('viewers')).order_by('-top_views')[:quantity].prefetch_related('viewers')

    return {'top_v_articles': top_v_articles}


@register.inclusion_tag('articles/recommended_articles.html')
def get_recommended_articles(quantity):
    """Вывод аниме из топа рекомендаций"""

    recs = RecArticle.objects.annotate(top=Count('users')).order_by('-top').values_list('article_id', flat=True)[:quantity]
    r_articles = Article.objects.filter(pk__in=recs)
    return {'r_articles': r_articles}

@register.simple_tag()
def get_dorams(quantity):
    return Article.objects.filter(category__link='dorama')[:quantity]


@register.inclusion_tag('articles/list_new_reviews.html')
def get_last_reviews():
    """Вывод последних комментариев на странице со списком аниме"""

    last_reviews = Review.objects.all()[:4]
    return {'last_reviews': last_reviews}