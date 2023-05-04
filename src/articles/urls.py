from django.urls import path, include
from src.articles.views import ArticleViewSet

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('articles/', ArticleViewSet.as_view({'get': 'list',}), name='article-list'),
    path('articles/<int:pk>/', ArticleViewSet.as_view({'get': 'retrieve',}), name='article-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)