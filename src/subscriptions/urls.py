from django.urls import path
from . import views

urlpatterns = [
    path('<slug:link>', views.SubscriptionView.as_view(), name='sub')
]