from django import template
from src.articles.models import Review, Article
from django.db.models import Count
from datetime import datetime, timedelta
register = template.Library()

@register.simple_tag()
def get_last_reviews():
    """Вывод последних комментариев на странице со списком аниме"""

    last_reviews = Review.objects.all()
    return {'last_reviews':last_reviews}


@register.simple_tag()
def get_last_articles():
    """Вывод последних добавленных аниме"""

    return Article.objects.all()[:4]


@register.simple_tag()
def get_top_views_articles():
    """Вывод аниме с наибольшими просмотрами """

    pass
    # print(Article.objects.annotate(top_views=Count('viewers')).order_by('-top_views')[:5].prefetch_related('viewers').explain())

    # curent_date = datetime.today()
    # start_date = curent_date - timedelta(days=5)

    # # print(Article.objects.filter(viewers__viewed_on__range=[start_date, curent_date]).values('viewers').order_by('-viewers')[:5])
    # print(Article.objects.filter(viewers__viewed_on__range=[start_date, curent_date]).annotate(top_views=Count('viewers')).order_by('-top_views').prefetch_related('viewers')[:5])
    return Article.objects.annotate(top_views=Count('viewers')).order_by('-top_views')[:5].prefetch_related('viewers')
    # Article.objects.all()[:5]