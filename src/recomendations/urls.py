from django.urls import path
from . import views

urlpatterns = [
    path('recs/<int:article>/<int:user>/', views.RecArticleCreateView.as_view(), name='create_recarticle')
]