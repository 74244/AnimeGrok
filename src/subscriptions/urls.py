from django.urls import path
from . import views

urlpatterns = [
    path('subs/<int:article>/<int:user>/', views.SubscriptionView.as_view(), name='add_subscription')
]