from typing import Any
from django import http
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, CreateView

from src.subscriptions.models import Subscription



#FIXME: Исправить редирект

class SubscriptionView(View):
    """Добавление аниме подписки"""

    model = Subscription

    def post(self, request, **kwargs):

        article = self.kwargs.get('article')
        user_pk = self.kwargs.get('user')
        url = request.META.get('HTTP_REFERER')
        user = self.model.objects.filter(user_id=user_pk, article_id=article).values()
        try:
            sub = get_object_or_404(user)
        except Exception:
            self.model.objects.create(user_id=user_pk, article_id=article)
            return HttpResponseRedirect(f'{url}')
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