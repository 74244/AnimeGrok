from rest_framework import serializers

from src.profiles.models import UserNet


class UserNetListSerializer(serializers.ModelSerializer):
    """Вывод списка профилей"""

    class Meta:
        model = UserNet
        fields = ("id", "username", "avatar")


class UserNetDetailSerializer(serializers.ModelSerializer):
    """
    Вывод информации о профиле
    """

    avatar = serializers.ImageField(read_only=True)

    class Meta:
        model = UserNet
        exclude = (
            "password",
            "last_login",
            "is_active",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
            "date_joined",
        )
