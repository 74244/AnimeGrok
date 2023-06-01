
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey

class Category(models.Model):
    """Категории"""

    name = models.CharField("Название", max_length=150)
    description = models.TextField("Описание", blank=True, null=True)
    link = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural= "Категории"


class Actor(models.Model):
    """Актеры озвучивания, тайминг и работали над субтитрами"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Актёр", on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to="actors/", blank=True)
    age = models.PositiveIntegerField("Возраст", default=0)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Актёр"
        verbose_name_plural= "Актёры"


class Genre(models.Model):
    """Жанры"""

    name = models.CharField("Название",max_length=100)
    description = models.TextField("Описание", blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        

class Viewer(models.Model):
    ip = models.GenericIPAddressField("IP address", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    viewed_on = models.DateTimeField("Дата просмотра",auto_now_add=True)

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"


class Article(models.Model):
    """Аниме"""

    ACTIVITY_LIST = (
        ('Продолжается', 'Продолжается'),
        ('Завершён', 'Завершён'),
        ('Airling', 'Airling'),
        ('Completed', 'Completed'),

    )
    title = models.CharField("Название", max_length=150)
    title_alt = models.CharField("Альтернативное название", max_length=150)
    description = models.TextField("Описание", blank=True)
    author = models.CharField("Автор", blank=True, null=True)
    type = models.CharField("Тип", max_length=150, null=True, blank=True)
    studio = models.CharField("Студия", max_length=150, null=True, blank=True)
    date_aired = models.DateField("Дата выхода в эфир")
    activity = models.CharField(verbose_name="Статус",choices=ACTIVITY_LIST, default='Продолжается')
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='article'
    )
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", blank=True, related_name='article')
    duration = models.CharField("Длительность", max_length=3)
    quality = models.CharField("Качество")
    viewers = models.ManyToManyField(Viewer, verbose_name="Просмотры")
    country = models.CharField("Страна", max_length=100, blank=True, null=True)
    voicing = models.ManyToManyField(
        Actor,
        verbose_name="Озвучивание",
        related_name='article_voicer',
        blank=True,
    )
    link = models.SlugField(max_length=150, unique=True, blank=True)
    poster = models.ImageField('Постер', upload_to='posters/', blank=True)
    timing = models.ManyToManyField(Actor, verbose_name='Тайминг', blank=True, related_name="timing_workers")
    subtitles = models.ManyToManyField(
        Actor,
        verbose_name="Работали над субтитрами",
        blank=True,
        related_name="subs_workers"
    )
    season = models.CharField("Сезон", max_length=150, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    series = models.CharField("Общее количество серий", default='XX')
    on_main = models.BooleanField("Отображать на главной", default=False)
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.link}) #, {"pk":self.id}

    def get_video_episodes(self):
        return Video.objects.filter(link=self.link)
    
    def get_review(self):
        data = self.review_set.filter(parent__isnull=True)
        return data

    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'
    
class ArticleShot(models.Model):
    """Кадры из аниме"""
    article = models.ForeignKey(Article, verbose_name='Аниме', on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=150)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='article_shots/')


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Кадр из аниме"
        verbose_name_plural = "Кадры из аниме"


class RatingStar(models.Model):
    """Звезда рейтинга"""

    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'
    
    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""

    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='звезда')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Аниме', related_name='ratings')

    def __str__(self):
        return f"{self.star} - {self.article}"
    
    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(MPTTModel):
    """Отзыв"""
    article = models.ForeignKey(Article, verbose_name="Аниме", on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField("Сообщение", max_length=5000)
    parent = TreeForeignKey(
        'self',
        verbose_name='Родительский комментарий',
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.author}:{self.text}'

    # @property
    # def get_avatar(self):
    #     if self.author:
    #         return self.author.profile.get_avatar
    #     return f'https://ui-avatars.com/api/?size=190&background=random&name={self.name}'
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Video(models.Model):
    """Модель загрузки видео"""

    article = models.ForeignKey(Article, verbose_name="Аниме", on_delete=models.CASCADE, related_name='article_episodes')
    episode = models.PositiveSmallIntegerField("Номер эпизода", blank=True)
    title = models.CharField("Название эпизода", blank=True, max_length=150)
    image = models.ImageField("Изображение", upload_to='images/', blank=True)
    file = models.FileField(
        upload_to='video/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
    )
    create_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.article}-{self.episode}-{self.title}"
    
    def get_absolute_url(self):
        return reverse("stream", kwargs={"slug":self.article.link, "episode": self.episode})
    
    class Meta:
        verbose_name_plural = "Видео"
        ordering = ('episode',)