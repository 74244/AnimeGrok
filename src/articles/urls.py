from django.views.decorators.cache import cache_page
from django.urls import path, include
from src.articles import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('add-rating/', views.AddRatingStar.as_view(), name='add-rating'),
    path('search/', views.Search.as_view(), name='search'),

    path('tv-filter/', views.TopViewsFilterView.as_view(), name='top_views_filter'),
    
    path('articles/', cache_page(60*10)(views.ArticleListView.as_view()), name='article-list'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<int:pk>/reviews/create/', views.ReviewCreateView.as_view(), name='create-review'),
]


