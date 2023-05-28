from django.db.models import Count
from rest_framework import serializers
from rest_framework.reverse import reverse

from src.articles.models import  Article, Video, Category, Actor, Genre, Rating, Review
from src.profiles.models import UserNet



class UserNetListSerializer(serializers.ModelSerializer):
    """Вывод списка профилей"""

    class Meta:
        model = UserNet
        fields = ("id", "username", "avatar")


class UserNetDetailSerializer(serializers.ModelSerializer):
    """
    Вывод информации о профиле
    """

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
    viewers_count = serializers.SerializerMethodField()
    link = serializers.HyperlinkedIdentityField(view_name='article-detail', lookup_field = 'link')

    class Meta:
        model = Article
        fields = ("id", "title", "category", "genres", "viewers_count", "link", "poster", "series", )

    def get_viewers_count(self, obj):
        return obj.viewers.count()
    


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Вывод и редактирование аниме/поста/релиза"""
    
    category = serializers.ReadOnlyField(source='category.name')
    genres = serializers.StringRelatedField(many=True)
    viewers_count = serializers.SerializerMethodField()
    link = serializers.HyperlinkedIdentityField(view_name='article-detail', lookup_field = 'link')
    video_episodes = serializers.SerializerMethodField()
    lookup_field = 'link'

    class Meta:
        model = Article
        fields = ("id", "title", "title_alt", "description", "author", "type", "studio", "date_aired", 
                  "activity", "category", "genres", "duration", "quality", "viewers_count", "coutry", 
                  "voicing", "link", "poster", "timing", "subtitles", "season", "series", 'video_episodes')
        
    def get_viewers_count(self, obj): # 4 запроса
            return obj.viewers.count()
    
    def get_video_episodes(self, obj): # 4 запроса
        episodes = {}
        ep = Video.objects.filter(article_id=obj.id)
        for item in ep:
            episodes[item.episode] = item.get_absolute_url()
        return episodes
     
        
class CategorySerializer(serializers.ModelSerializer):
    """Категории"""

    class Meta:
        model = Category
        fields = ("id", "name", "description", "link")

class ActorSerializer(serializers.ModelSerializer):
    """ Актеры """

    class Meta:
        model = Actor
        fields = ("name", "description", "image", "age")

class GenreSerializer(serializers.ModelSerializer):
    """Жанры"""

    class Meta:
        model = Genre
        fields = ("name")

class RatingSerializer(serializers.ModelSerializer):
    """Рейтинг"""

    class Meta:
        model = Rating
        fields = ("article", "star")

class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы"""

    class Meta:
        model = Review
        fields = ("user", "article", "text", "parent", "create_at")

# class VideoSerializer(serializers.ModelSerializer):
#     """Видео эпизоды"""

#     class Meta:
#         model = Video
#         fields = ("id", "episode", "get_absolute_url")
    
#     def get_queryset(self):
#         return Video.objects.filter(pk=self.pk)