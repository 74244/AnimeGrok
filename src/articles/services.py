from collections import OrderedDict
from datetime import datetime, timedelta
from pathlib import Path
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from modeltranslation.manager import MultilingualQuerySet
from src.articles.models import Video, Article
from src.recomendations.models import RecArticle

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

class ArticleService:
    def get_data(self, qset: MultilingualQuerySet, quantity: None):
        pass
    def get_season(self, month: datetime.month):
        pass

class ArticleListService(ArticleService):
    def __init__(self, qset: MultilingualQuerySet):
        self.queryset = qset

    def get_hsa(self, quantity) -> MultilingualQuerySet:
        """Список аниме на главную для слайдера"""

        hsa = self.queryset.filter(on_main=True).only('title', 'link', 'genres','poster').prefetch_related('genres')[:quantity]
        return hsa
    
    def get_sa(self, quantity) -> MultilingualQuerySet:
        """ Вывод аниме по сезону """

        sa = self.queryset.prefetch_related('viewers', 'genres', 'videos').filter(season__contains='2023-Весна').only('title', 'link', 'genres__name', 'viewers', 'season', 'series', 'poster')[:quantity]
        return sa
    
    def get_la(self, quantity) -> MultilingualQuerySet:
        """Вывод последних добавленных аниме"""

        data = Video.objects.values_list('article_id', flat=True).order_by('-create_at')
        res = list(OrderedDict.fromkeys(data))
        last_arts = self.queryset.prefetch_related('viewers', 'genres', 'videos').filter(pk__in=res).only('title', 'link', 'genres', 'viewers', 'season', 'series', 'poster')[:quantity]
        return last_arts
    
    def get_tva(self, quantity) -> MultilingualQuerySet:
        """Вывод аниме с наибольшими просмотрами """

        tva = self.queryset.annotate(top_views=Count('viewers')).order_by('-top_views')[:quantity].prefetch_related('viewers', 'videos').only('title', 'link', 'viewers', 'series', 'poster')
        return tva
    
    def get_rec_arts(self, quantity) -> MultilingualQuerySet:
        recs = RecArticle.objects.annotate(top=Count('users')).order_by('-top').values_list('article_id', flat=True)[:quantity]
        rec_articles = self.queryset.prefetch_related('genres', 'viewers', 'videos').filter(pk__in=recs).only('title', 'link', 'genres', 'viewers', 'season', 'series', 'poster')
        return rec_articles
    
    def get_dorams(self, quantity) -> MultilingualQuerySet:
        dorams = self.queryset.prefetch_related('viewers', 'genres', 'videos').filter(category__link='dorama').only('title', 'link', 'viewers', 'series', 'poster')[:quantity]
        return dorams

def check_date():
    curent_date = datetime.today()
    start_date = curent_date - timedelta(days=5)
    queryset = Article.objects.filter(viewers__viewed_on__range=[start_date, curent_date]).values('viewers').order_by('-viewers')[:5]

#TODO: Добавить уведомления в результате функции
def check_article_user(self, request, **kwargs):
    """Проверка подписки и рекомендаций"""
    
    article = self.kwargs.get('article')
    user_pk = self.kwargs.get('user')
    url = request.META.get('HTTP_REFERER')
    try :
        self.model.objects.get(article_id=article, users=user_pk)
    except ObjectDoesNotExist:
        self.model.objects.create(article_id=article).users.add(user_pk)
    finally:
        return url