from django.db import models

# Create your models here.
class Category(models.Model):
    """Категории"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание", blank=True, null=True)
    link = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural= "Категории"

class Actor(models.Model):
    """Актеры озвучивания, тайминг и работали над субтитрами"""
    name = models.CharField()
    description = models.TextField("Описание", blank=True, null=True)
    image = models.ImageField("Изображение", upload_to="actors/")
    age = models.PositiveIntegerField("Возраст", default=0)

class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя",max_length=100)
    description = models.TextField("Описание", blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Ip(models.Model):
    ip = models.CharField(max_length=100)

class Article(models.Model):
    """Аниме"""
    ACTIVITY_LIST = (
        ('Продолжается', 'Продолжается'),
        ('Завершён', 'Завершён'),

    )
    title = models.CharField("Название", max_length=150)
    title_alt = models.CharField("Альтернативное название", max_length=150)
    description = models.TextField("Описание", blank=True)
    author = models.CharField("Автор", blank=True, null=True)
    type = models.CharField("Тип", max_length=150, null=True, blank=True)
    studio = models.CharField("Студия", max_length=150, null=True, blank=True)
    date_aired = models.DateField("Дата выхода в эфир")
    activity = models.CharField(verbose_name="Тип",choices=ACTIVITY_LIST, default='Продолжается')
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", blank=True)
    duration = models.CharField("Длительность", max_length=3)
    quality = models.CharField("Качество")
    views = models.IntegerField("Просмотры", default=0)
    coutry = models.CharField("Страна", max_length=100, blank=True, null=True)
    voicing = models.ManyToManyField(Actor, verbose_name="Озвучивание", related_name='article_voicer', blank=True)
    link = models.SlugField(max_length=150, unique=True, blank=True)
    poster = models.ImageField('Постер', upload_to='posters/', blank=True)
    timing = models.ManyToManyField(Actor, verbose_name='Тайминг', blank=True, related_name="timing_workers")
    subtitles = models.ManyToManyField(Actor, verbose_name="Работали над субтитрами", blank=True, related_name="subs_workers")
    season = models.CharField("Сезон", max_length=150, blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'
    
class ArticleShot(models.Model):
    """Кадры из аниме"""
    title = models.CharField("Заголовок", max_length=150)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='article_shots/')
    article = models.ForeignKey(Article, verbose_name='Аниме', on_delete=models.CASCADE)

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

class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    article = models.ForeignKey(Article, verbose_name="Аниме", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.article}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"