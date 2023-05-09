from django.db import models
from django.conf import settings
from src.articles.models import Article


class Subscription(models.Model):
    """Подписка пользователя на аниме"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="users",
    )
    article = models.ForeignKey(
        Article,
        verbose_name="Аниме",
        on_delete=models.CASCADE,
        related_name="sub_articles"
    )
