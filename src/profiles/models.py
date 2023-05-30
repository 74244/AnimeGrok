from django.db import models
from django.contrib.auth.models import AbstractUser


from src.articles.models import Article

class UserNet(AbstractUser):
    ADMIN = 'admin'
    VOICER = 'voicer'
    TIMER = 'timer'
    TRANSLATOR = 'subtitles'
    USER = 'user'
    ROLES_CHOICES = (
        (ADMIN, "Администратор"),
        (VOICER, 'Озвучка'),
        (TIMER, 'Тайминг'),
        (TRANSLATOR, 'Переводчик'),
        (USER, 'Пользователь'),
    )
    GENDER = (('М', 'male'),('Ж', 'female'))
    bio = models.TextField("О себе",blank=True, null=True)
    phone = models.CharField("Телефон",max_length=14, blank=True, null=True)
    avatar = models.ImageField("Изображение",upload_to="user/avatar",  null=True, blank=True)
    link = models.URLField("Ссылка", blank=True, null=True)
    birthday = models.DateField("Дата рождения", blank=True, null=True)
    gender = models.CharField("Пол", max_length=6, choices=GENDER, default='male')
    subscriptions = models.ManyToManyField(
        Article, verbose_name="Подписки", related_name='users', blank=True
    )
    status = models.CharField("Статус", max_length=50, help_text="Выберите статус пользователя", choices=ROLES_CHOICES, default='user')

    @property
    def is_admin(self):
        return self.status == self.ADMIN
    
    @property
    def is_voicer(self):
        return self.status == self.VOICER
    
    @property
    def is_timer(self):
        return self.status == self.TIMER
    
    @property
    def is_translator(self):
        return self.status == self.TRANSLATOR
    
    
    def __str__(self):
        return self.username
    

    class Meta:
        verbose_name = ("Пользователь")
        verbose_name_plural = ("Пользователи")
    
