from django.db import models
from django.conf import settings
from src.articles.models import Article


class Subscription(models.Model):
    """Подписка пользователя на аниме"""
    article = models.ForeignKey(
        Article,
        verbose_name="Аниме",
        on_delete=models.CASCADE,
        related_name="sub_articles"
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователи",
        related_name="subs",
        blank=True
    )

    class Meta:
        verbose_name_plural = "Подписки на аниме"
