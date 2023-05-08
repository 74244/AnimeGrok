from typing import Any

from django.db import models
from django.http import StreamingHttpResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView, View

from .models import Article, Video

from .services import open_file


def home(request):
    return render(request, 'home.html')
    

class ArticleListView(ListView):
    model = Article
    paginate_by = 9
    template_name = "articles/article-list.html"

class ArticleDetailView(DetailView):
    model = Article
    queryset = Article.objects.all()
    template_name = "articles/article-details.html"
    context_object_name = 'article'
    

#TODO: доделать форму после реализации аутентификации
class AddReview(View):
    """Добавление отзыва"""
    def post(self, request, pk):
        pass

def get_streaming_video(request, pk, episode: int):
    file, status_code, content_lenght, content_range = open_file(request, pk, episode)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_lenght)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range

    return response



# {% url 'video' video.id %}


