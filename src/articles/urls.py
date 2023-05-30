from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('add-rating/', views.AddRatingStar.as_view(), name='add-rating'),
    path('search/', views.Search.as_view(), name='search'),

    path('tv-filter/', views.TopViewsFilterView.as_view(), name='top_views_filter'),
    
    path('articles/', views.ArticleListView.as_view(), name='article-list'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<slug:slug>/episode-<int:episode>/', views.get_streaming_video, name='stream'),
    path('articles/<int:pk>/reviews/create/', views.ReviewCreateView.as_view(), name='create-review'),
]


