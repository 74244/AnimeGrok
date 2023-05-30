from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from src.articles.services import check_article_user
from src.recomendations.models import RecArticle
# Create your views here.

class RecArticleCreateView(View):
    """Добавление аниме подписки"""

    model = RecArticle

    def post(self, request, **kwargs):
        url = check_article_user(self, request, **kwargs)
        return HttpResponseRedirect(f'{url}')