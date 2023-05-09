from django.urls import path
from . import views

urlpatterns = [
    path('<int:article_pk>', views.SubscriptionView.as_view(), name='sub')
]