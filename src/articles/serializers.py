from rest_framework import serializers

from .models import Article, Genre

class ArticleListSerializer(serializers.ModelSerializer):
    """Вывод списка аниме"""

    class Meta:
        model  = Article
        fields = ("id", "title", "poster")

class ArticleDetailSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(source='category.name', read_only=True)
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Article
        exclude = (
            'link',
            'views',
            'poster',
        )