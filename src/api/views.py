from django.shortcuts import render

from rest_framework import generics, permissions, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer, BrowsableAPIRenderer

from src.api.serializers import (ArticleListSerializer, ArticleDetailSerializer,
                                 UserNetListSerializer, UserNetDetailSerializer,
                                 CategorySerializer, ActorSerializer, GenreSerializer,
                                 RatingSerializer, ReviewSerializer, VideoSerializer
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

class ActorViewSet(viewsets.ModelViewSet):
    """Актёры"""

    serializer_class = ActorSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Actor.objects.all()
    
class GenreViewSet(viewsets.ModelViewSet):
    """Жанры"""

    serializer_class = GenreSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Genre.objects.all()
    

class RatingViewSet(viewsets.ModelViewSet):
    """Рейтинг"""

    serializer_class = RatingSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Rating.objects.all()



#TODO Сделать рекурсив по отзывам
class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы"""

    serializer_class = ReviewSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Video.objects.all()