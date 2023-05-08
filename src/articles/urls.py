from django.urls import path, include
from . import views


urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article-details'),
    path('articles/<int:pk>/episode-<int:episode>/', views.get_streaming_video, name='stream'),
    path('', views.home, name='home-page'),
]

