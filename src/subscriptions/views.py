from typing import Any
from django import http
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView

from src.articles.services import check_article_user
from src.subscriptions.models import Subscription



#FIXME: Исправить редирект

class SubscriptionView(View):
    """Добавление аниме подписки"""

    model = Subscription

    def post(self, request, **kwargs):
        url = check_article_user(self, request, **kwargs)
        return HttpResponseRedirect(f'{url}')
    
#TODO: Исправить удаление
    # def delete(self, request, *args):
    #     article = self.kwargs.get('article')
    #     user = self.kwargs.get('user')
    #     url = self.kwargs.get('url')
        
    #     sub = self.model.objects.get(article=article, user_id=user)
    #     print(f"del-sub = {sub}")
    #     sub.delete()
    #     return HttpResponseRedirect(f'{url}')