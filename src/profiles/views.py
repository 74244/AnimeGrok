
from django.shortcuts import render
from django.views.generic import ListView

from rest_framework import permissions, generics
from rest_framework.viewsets import ModelViewSet


from src.profiles.models import UserNet
from src.profiles.serializers import UserNetListSerializer, UserNetDetailSerializer

class UserNetViewSet(ModelViewSet):
    """
    Вывод профиля пользователя
    """
    queryset = UserNet.objects.all()

    # permission_classes = [permissions.AllowAny]  # заменить на аутентифицированного

    def get_serializer_class(self):
        if self.action == "list":
            return UserNetListSerializer
        elif self.action == "retrieve":
            return UserNetDetailSerializer
        
