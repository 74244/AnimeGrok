from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from src.articles.models import Article
from src.articles.serializers import ArticleListSerializer, ArticleDetailSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    """Вывод списка аниме"""
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        if self.action == "retrieve":
            return ArticleDetailSerializer
