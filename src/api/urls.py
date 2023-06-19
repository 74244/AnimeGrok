from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from src.api.views import (ArticleViewSet, UserNetViewSet, CategoryViewSet, 
                           ActorViewSet,GenreViewSet, RatingViewSet,
                           ReviewViewSet, VideoViewSet, ArticleTopViewersView,
                           RecArticleViewSet)
from src.routers import CustomArticleRouter, CustomTopViewsArticleRouter

router = routers.SimpleRouter()
a_router = CustomArticleRouter()
tva_router = CustomTopViewsArticleRouter()

a_router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'profiles', UserNetViewSet, basename='profile')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'article-recomendations', RecArticleViewSet, basename='recarticle')

urlpatterns = router.urls

urlpatterns = [
    path('articles/topviews/', ArticleTopViewersView.as_view()),
    path('', include(a_router.urls))
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)