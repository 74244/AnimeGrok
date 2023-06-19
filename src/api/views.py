from django.db import connection
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, mixins, viewsets, filters, pagination

from src.api.serializers import (ArticleListSerializer, ArticleDetailSerializer,
                                 UserNetListSerializer, UserNetDetailSerializer,
                                 CategorySerializer, ActorSerializer, GenreSerializer,
                                 RatingSerializer, ReviewSerializer, VideoSerializer,
                                 RecArticleSerializer)

from src.api.permissions import IsStaffAdminOrReadOnly

from src.articles.models import Article, Category, Actor, Genre, Rating, Review, Video
from src.profiles.models import UserNet
from src.recomendations.models import RecArticle


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

    permission_classes = [IsStaffAdminOrReadOnly]
    # permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('title', 'date_aired', 'category', 'genres')
    lookup_field = 'link'
    
    def get_queryset(self):
        if self.action == 'list':
            return  Article.objects.all().select_related('category').prefetch_related('viewers', 'genres', 'article_episodes', 'article_recs').only('title', 'link', 'viewers', 'series', 'poster', 'date_aired', 'genres', 'category', 'season')
        else:
            return Article.objects.select_related('category', 'user').all().prefetch_related('viewers', 'genres', 'article_episodes', 'voicing', 'timing', 'subtitles', 'videos')
  
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        else:
            return ArticleDetailSerializer
        

class ArticleTopViewersView(generics.ListAPIView):
    """Аниме релизы по количеству просмотров"""

    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ('category', 'date_aired', 'genres')
    search_fields = ('title',)

    def get_queryset(self):
        qset = Article.objects.all().select_related('category').prefetch_related('viewers', 'article_episodes', 'genres', 'article_recs').only('title', 'link', 'viewers', 'series', 'poster', 'date_aired', 'genres', 'category', 'season')
        print(qset.values('article_recs')[:1])
        return qset    


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
        return Actor.objects.all().select_related('user')
    
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
        return Rating.objects.all().select_related('article', 'star')


#TODO Сделать рекурсив по отзывам
class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы"""

    serializer_class = ReviewSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Review.objects.all().select_related('article', 'author', 'parent')
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class VideoViewSet(viewsets.ModelViewSet):
    """Видео"""

    serializer_class = VideoSerializer
    permission_classes = [IsStaffAdminOrReadOnly]

    def get_queryset(self):
        return Video.objects.all().select_related('article')
    

class RecArticleViewSet(viewsets.ModelViewSet):
    """Рекомендации"""

    serializer_class = RecArticleSerializer

    def get_queryset(self):
        return RecArticle.objects.select_related('article', 'user')