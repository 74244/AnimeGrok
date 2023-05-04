from django.urls import path, include

from src.profiles.views import UserNetViewSet

from rest_framework.urlpatterns import format_suffix_patterns
profile_detail = UserNetViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    # 'patch': 'partial_update',
    # 'delete': 'destroy'
})


urlpatterns = [
    path('profiles/', UserNetViewSet.as_view({'get':'list'}), name='profile-list'),
    path('profiles/<int:pk>/', profile_detail, name='profile-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)