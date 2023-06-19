import datetime
from django.core.files import File
from django.test import Client, TestCase, override_settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_factory_boy.tests import factory
from mock import MagicMock
from src.articles.models import (Category, Actor, Genre, Viewer, Article, 
                                 ArticleShot, Rating, Review, Video)

User = get_user_model()
video_mock = MagicMock(spec=File)
video_mock.name = 'testvideo.mp4'

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = 'Test'
    password = 'test'
    is_superuser = True
    is_active = True



class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    name='Testing Category'
    description='Test description'
    link='testing-category'
    
        
class ActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Actor
    user = factory.SubFactory(UserFactory)
    description = 'Test Actor Description'
    image = factory.django.ImageField(color='blue')
    age = 25
        

class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre
    name = 'TestingGenre'
    description = 'Test Genre Description' 
    slug = 'testinggenre'

class ViewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Viewer
    ip = '1.1.1.1'
    user = factory.SubFactory(UserFactory)

class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article
    
    title='Test Title',
    title_alt='Testus Titlus',
    description='Описание',
    author='Автор',
    type='TV',
    studio='Студия',
    date_aired='2023-01-01',
    category=factory.SubFactory(CategoryFactory)
    duration='12',
    quality='4K',
    country='Япония',
    link='testus-titlus',
    poster=factory.django.ImageField(color='blue')
    season='Winter-2022',
    user = factory.SubFactory(UserFactory)
    series='12',
    on_main=True,

    @factory.post_generation
    def viewers(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for viewer in extracted:
                self.viewers.add(viewer)

class ArticleShotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ArticleShot

    article = factory.SubFactory(ArticleFactory)
    title = 'Test ArticleShot'
    description = 'Test Description'
    image = factory.django.ImageField(color='blue')


# # class ArticleTestCase(TestCase):
# class ArticleTestCase(TestCase):
#     def setUp(self) -> None:
#         self.client = Client()
        
#         image_mock = MagicMock(spec=File)
#         image_mock.name = 'image.png'
        
#         video_mock = MagicMock(spec=File)
#         video_mock.name = 'video.mp4'

#         user_article= User.objects.create(username='articleuser')
#         user_view = User.objects.create(username='vuser')
#         user_voice = User.objects.create(username='voicer1')
#         user_time = User.objects.create(username='timer1')
#         user_sub = User.objects.create(username='sub1')

#         voicer = Actor.objects.create(user=user_voice)                                        #
#         timer = Actor.objects.create(user=user_time)                                        #
#         sub = Actor.objects.create(user=user_sub)

#         category_art = Category.objects.create(name='Категория', link='category')
#         genre = Genre.objects.create(name='Хоррор', slug='horror')                                             #
#         viewer = Viewer.objects.create(ip='127.0.0.1', user=user_view)     #

#         article = Article.objects.create(
#             title='Test Title',
#             title_alt='Testus Titlus',
#             description='Описание',
#             author='Автор',
#             type='TV',
#             studio='Студия',
#             date_aired='2023-01-01',
#             category=category_art,
#             duration='12',
#             quality='4K',
#             country='Япония',
#             link='testus-titlus',
#             poster=image_mock.name,
#             season='Winter-2022',
#             user=user_article,
#             series='12',
#             on_main=True,
#         )
#         ag = article.genres
#         ag.add(genre)
#         article.viewers.add(viewer)
#         article.voicing.add(voicer)
#         article.timing.add(timer)
#         article.subtitles.add(sub)
        
#         video=Video.objects.create(article=article, episode=1, title='Название', 
#                             image=image_mock.name, file=video_mock.name)
        
#         article.videos.add(video)

#         review = Review.objects.create(article=article, author=user_article, text='Text review')
#         review2 = Review.objects.create(article=article, author=user_voice, text='Text review2', parent=review)


#     def test_link_slug(self):
#         article = Article.objects.get(title='Test Title')
#         self.assertEqual(article.link, 'testus-titlus')

#     def test_on_main(self):
#         article = Article.objects.get(link='testus-titlus')
#         self.assertEqual(article.on_main, True)

#     def test_get_response(self):
#         response = self.client.get('')
#         self.assertEqual(response.status_code, 200)
    
#     def test_count(self):
#         response = self.client.get('', {'season': 'Winter-2022'}, {'county': 'Япония'})
#         self.assertEqual(response.status_code, 200)

#     def test_m2m_response(self):
#         response = self.client.get('', 
#             {'genres': 1},
#             {'viewers': 1},
#             {'voicing': 1},
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_m2m_response2(self):
#         response = self.client.get('', 
#             {'timing': 1},
#             {'subtitles': 1},
#             {'videos': 1}
#         )
#         self.assertEqual(response.status_code, 200)

#     def test_get_absolute_url(self):
#         article = Article.objects.get(title_alt='Testus Titlus')
#         self.assertEqual(article.get_absolute_url(), '/articles/testus-titlus/')

#     def test_get_reviews(self):
#         article = Article.objects.get(title_alt='Testus Titlus')
#         author = article.author.id
#         reviews_list = article.reviews.all()
#         review = reviews_list[0]
        
#         self.assertEqual(review.article, article)
#         self.assertEqual(review.author, author)
#         self.assertEqual(review.text, 'Text review')
        
#         self.assertEqual(len(reviews_list), 2)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    article = factory.SubFactory(ArticleFactory)
    author = factory.SubFactory(UserFactory)
    text = 'Test Review text'
    create_at = '2023-01-01'

class VideoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Video
    article = factory.SubFactory(ArticleFactory)
    episode = 1
    title = 'Test Video title'
    image = factory.django.ImageField(color='black')
    file = video_mock.name
    create_at = '2023-01-01'
