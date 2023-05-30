from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from src.api.views import (ArticleViewSet, UserNetViewSet, CategoryViewSet, 
                           ActorViewSet,GenreViewSet, RatingViewSet,
                           ReviewViewSet, VideoViewSet)
from src.routers import CustomArticleRouter

# import pprint
# pp = pprint.PrettyPrinter(indent=4)

router = routers.SimpleRouter()
a_router = CustomArticleRouter()

a_router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'profiles', UserNetViewSet, basename='profile')


router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'videos', VideoViewSet, basename='video')

urlpatterns = router.urls

# article_set = ArticleViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# profile_detail = UserNetViewSet.as_view({
#     'get': 'retrieve',
#     # 'put': 'update',
#     # 'patch': 'partial_update',
#     # 'delete': 'destroy'
# })
urlpatterns = [
    path('', include(a_router.urls))
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)