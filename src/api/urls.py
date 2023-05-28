from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from src.api.views import ArticleViewSet, UserNetViewSet, CategoryViewSet
from src.routers import CustomArticleRouter

# import pprint
# pp = pprint.PrettyPrinter(indent=4)

router = routers.SimpleRouter()
a_router = CustomArticleRouter()

a_router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'profiles', UserNetViewSet, basename='profile')


router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'actors', UserNetViewSet, basename='actor')
# router.register(r'genres', UserNetViewSet, basename='genre')
# router.register(r'ratings', UserNetViewSet, basename='rating')
# router.register(r'reviews', UserNetViewSet, basename='review')
# router.register(r'videos', UserNetViewSet, basename='video')

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