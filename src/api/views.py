from django.shortcuts import render

from rest_framework import generics, permissions, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer

from src.api.serializers import (ArticleListSerializer, ArticleDetailSerializer,
                                 UserNetListSerializer, UserNetDetailSerializer,
                                 CategorySerializer, 
                                )

from src.api.permissions import IsStaffAdminOrReadOnly

from src.articles.models import Article, Category, Actor, Genre, Rating, Review, Video
from src.profiles.models import UserNet

class UserNetViewSet(viewsets.ModelViewSet):
    """Пользователи"""

    queryset = UserNet.objects.all()

    # permission_classes = [permissions.AllowAny]  # заменить на аутентифицированного

    def get_serializer_class(self):
        if self.action == "list":
            return UserNetListSerializer
        else:
            return UserNetDetailSerializer
        
class ArticleViewSet(viewsets.ModelViewSet):
    """Аниме релизы"""

    lookup_field = 'link'
    permission_classes = [IsStaffAdminOrReadOnly]
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        if self.action == 'list':
            return  Article.objects.all().prefetch_related('viewers', 'genres').select_related('category', 'user',)
        else:
            return Article.objects.all()
        
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        else:
            return ArticleDetailSerializer

#TODO Проверить пермишины для не админов
class CategoryViewSet(viewsets.ModelViewSet):
    """Категории"""
    
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CategorySerializer
    def get_queryset(self):
        return Category.objects.all()

