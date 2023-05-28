from django.db import models
from django.contrib.auth.models import AbstractUser


from src.articles.models import Article

class UserNet(AbstractUser):
    GENDER = (('male', 'male'),('female', 'female'))
    bio = models.TextField("О себе",blank=True, null=True)
    phone = models.CharField("Телефон",max_length=14, blank=True, null=True)
    avatar = models.ImageField("Изображение",upload_to="user/avatar",  null=True, blank=True)
    link = models.URLField("Ссылка", blank=True, null=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    gender = models.CharField("Пол", max_length=6, choices=GENDER, default='male')
    subscriptions = models.ManyToManyField(
        Article, verbose_name="Подписки", related_name='users', blank=True
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = ("Пользователь")
        verbose_name_plural = ("Пользователи")
    
