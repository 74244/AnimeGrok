from django.urls import path, include, re_path

from rest_framework import permissions
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="AnimeGrok API",
        default_version='v1',
        description='Docs',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

class CustomArticleRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^articles/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^articles/{lookup}/$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail', }
        ),
        # DynamicRoute(
        #     url=r'^articles/{lookup}/episode-{url_path}$',
        #     name='{basename}-{url_name}',
        #     detail=True,
        #     initkwargs={}
        # )
    ]


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include('src.api.urls')),
    path('', include('src.articles.urls')),
    # path('', include('src.profiles.urls')),
    path('', include('src.subscriptions.urls')),
    path('', include('src.recomendations.urls')),
]

