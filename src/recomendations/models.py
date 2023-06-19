from django.db import models
from django.conf import settings
from src.articles.models import Article


class Recomendation(models.Model):
    """Подписка пользователя на аниме"""

    text = models.TextField(max_length=500, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class RecArticle(Recomendation):
    article = models.ForeignKey(
        Article,
        verbose_name="Аниме",
        related_name='article_recs',
        on_delete=models.CASCADE,
        blank=True,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        verbose_name="Пользователь", on_delete=models.CASCADE, related_name='article_rec_user')

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name_plural = 'Рекомендации аниме'


