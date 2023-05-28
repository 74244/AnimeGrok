from typing import Any, Dict

from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View

from src.base.mixins import CountViewerMixin
from src.profiles.models import UserNet
from .forms import RatingForm, ReviewForm
from .models import Article, Rating, RatingStar, Viewer, Genre
from .services import open_file
from datetime import datetime, timedelta


def home(request):
    return render(request, 'home.html')

class Genre:
    """ Жанры """

    def get_genres(self):
        return Genre.objects.all()

class ArticleListView(Genre, ListView):
    """Список аниме"""
    
    model = Article
    queryset = Article.objects.all().prefetch_related('viewers', 'genres').select_related('category', 'user',)#.only('title', 'link', 'poster', 'series', 'genres', 'viewers', 'category')
    template_name = "articles/article-list.html"
    paginate_by = 9


class ArticleDetailView(DetailView, CountViewerMixin):
    """Полное описание аниме"""

    model = Article
    # queryset = Article.objects.all()
    template_name = "articles/article-details.html"
    slug_field = 'link'
    context_object_name = 'article'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['review_form'] = ReviewForm()
        context['ip'] = self.get_mixin_ip(self.request)

        return context

class AddRatingStar(View, CountViewerMixin):
    """Добавление рейтинга к аниме"""
    
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                
                article_id=int(request.POST.get('article')),
                defaults={'star_id':int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


#TODO: доделать форму после реализации аутентификации
class AddReview(View):
    """Добавление отзыва"""

    def post(self, request, slug):
        form = ReviewForm(request.POST)
        article = Article.objects.get(link=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.user = request.user
            form.article = article
            form.save()
        return redirect(article.get_absolute_url())


#TODO: Сделать норм плеер

def get_streaming_video(request, slug, episode):
    pk = Article.objects.filter(link=slug).values('pk')[0]['pk']
    file, status_code, content_lenght, content_range = open_file(request, pk, episode) #episode)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_lenght)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response

class Search(ListView):
    """Поиск Аниме"""

    template_name = "articles/article-list.html"
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.filter(title__icontains=self.request.GET.get("q"))
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get("q")
        return context
    
class TopViewsFilterView(ListView):
    """Фильтр аниме в json"""

    def get_queryset(self):
        print(self.request.GET.lists())
        # if date_value == 'year':
        #     value = 365
        # if date_value == 'month':
        #     value = 365
        # if date_value == 'week':
        #     value = 7
        # curent_date = datetime.today()
        # start_date = curent_date - timedelta(days=value)
        # queryset = Article.objects.annotate(top_views=models.Count('viewers')).order_by('-top_views')[:5].prefetch_related('viewers')
        queryset = Article.objects.all()[:5].values('title', 'poster', 'viewers',)
        print(queryset)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return JsonResponse({'top_v_articles':list(queryset)})

