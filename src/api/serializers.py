from django.db import connection
from django.db.models import Count
from rest_framework import serializers
from rest_framework.reverse import reverse

from src.articles.models import  Article, Video, Category, Actor, Genre, Rating, Review
from src.profiles.models import UserNet
from src.recomendations.models import RecArticle


class UserNetListSerializer(serializers.ModelSerializer):
    """Вывод списка профилей"""

    class Meta:
        model = UserNet
        fields = ("id", "username", "avatar")


class UserNetDetailSerializer(serializers.ModelSerializer):
    """Вывод информации о профиле """

    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserNet
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "date_joined",
        )
    

class ArticleListSerializer(serializers.ModelSerializer):
    """Список аниме на странице"""

    category = serializers.ReadOnlyField(source='category.name')
    genres = serializers.StringRelatedField(many=True)
    viewers = serializers.SerializerMethodField()
    link = serializers.HyperlinkedIdentityField(view_name='article-detail', lookup_field = 'link')
    poster = serializers.SerializerMethodField()
    last_episode = serializers.SerializerMethodField()
    recomendations = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ("id", "title", "category", "genres", "viewers", "link", "poster", "series", "date_aired", 'last_episode', 'season', 'recomendations')

    def get_viewers(self, obj):
        return obj.viewers.count()

    def get_poster(self, article):
        if article and hasattr(article, 'poster'):
            return article.poster.url
        else:
            return None
    def get_last_episode(self, obj):
        return obj.article_episodes.count()
    
    def get_recomendations(self, obj):
        return obj.article_recs.count()
    

class ArticleDetailSerializer(serializers.ModelSerializer):
    """Вывод и редактирование аниме/поста/релиза"""

    category = serializers.ReadOnlyField(source='category.name')
    genres = serializers.StringRelatedField(many=True)
    viewers = serializers.SerializerMethodField()
    last_episode = serializers.SerializerMethodField()
    recomendations = serializers.SerializerMethodField()
    link = serializers.HyperlinkedIdentityField(view_name='article-detail', lookup_field = 'link')

    class Meta:
        model = Article
        fields = ("id", "title", "title_alt", "description", "author", "type", "studio", "date_aired", 
                  "activity", "category", "genres", "duration", "quality", "viewers", "country", 
                  "voicing", "link", "poster", "timing", "subtitles", "season", "series", 'last_episode', 'recomendations')
        
    def get_viewers(self, obj):
            return obj.viewers.count()
    def get_last_episode(self, obj):
        return obj.article_episodes.count()
    def get_recomendations(self, obj):
        return obj.article_recs.count()
        

class CategorySerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Category
        fields = ("id", "name", "description", "link")


class ActorSerializer(serializers.ModelSerializer):
    """ Актеры """

    user = serializers.StringRelatedField(source = 'user.username')
    status = serializers.StringRelatedField(source = 'user.status')

    class Meta:
        model = Actor
        fields = ("user", "status", "description", "image", "age")
    

class GenreSerializer(serializers.ModelSerializer):
    """Жанры"""

    class Meta:
        model = Genre
        fields = ("name",)

class RatingSerializer(serializers.ModelSerializer):
    """Рейтинг"""
    article = serializers.ReadOnlyField(source='article.title')
    class Meta:
        model = Rating
        fields = ("article", "star")


class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы"""
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Review
        fields = ("user", "article", "text", "create_at")
    

class VideoSerializer(serializers.ModelSerializer):
    """Видео эпизоды"""

    article = serializers.StringRelatedField(source="article.title")
    video = serializers.SerializerMethodField()


    class Meta:
        model = Video
        fields = ("article","episode","title", "image", 'video')

    def get_video(self, obj):
        return obj.get_absolute_file_url()
    

class RecArticleSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField(source="article.title")
    user = serializers.StringRelatedField(source="user.username")
    
    class Meta:
        model = RecArticle
        fields = ('article', 'user', 'text')