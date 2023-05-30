from django.db import models
from django.conf import settings
from src.articles.models import Article


class Recomendation(models.Model):
    """Подписка пользователя на аниме"""

    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
        verbose_name="Пользователи", blank=True)
    text = models.TextField(max_length=500, blank=True)

    class Meta:
        abstract = True

class RecArticle(Recomendation):
    article = models.ForeignKey(
        Article,
        verbose_name="Аниме",
        on_delete=models.CASCADE,
        blank=True
    )

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name_plural = 'Рекомендации аниме'