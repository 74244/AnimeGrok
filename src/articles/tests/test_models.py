import datetime
import django
import os
import slugify

from django.contrib.auth import get_user_model
from django.core.files import File
from django_factory_boy.tests import factory
from django.test import Client, TestCase
from mock import MagicMock

from src.articles.tests.factories import (UserFactory, CategoryFactory, ActorFactory, GenreFactory, ViewerFactory, ArticleFactory, ArticleShotFactory, ReviewFactory, VideoFactory)
from src.articles.services import pp

User = get_user_model()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


class CategoryTestCase(TestCase):
    def test_name(self):
        category = CategoryFactory.build(name='TestCat')
        self.assertEqual(category.name, category.name)

    def test_description(self):
        category = CategoryFactory.build(description='Test description in testcase')
        self.assertEqual(category.description, category.description)

    def test_link(self):
        category = CategoryFactory.build(name='TestCatLink', link='testcatlink')
        self.assertEqual(category.link, category.link)

    def test_str_return(self):
        category = CategoryFactory.build(name='TestStrReturn')
        self.assertEqual(category.__str__() , category.name)


class ActorTestCase(TestCase):

    def test_user(self):
        new_user = UserFactory.build(username='testactor')
        actor = ActorFactory.build(user=new_user, age=35)
        self.assertEqual(actor.user, new_user)
        
    def test_description(self):
        test_description='Test Actor Description'
        actor = ActorFactory.build(description=test_description)
        self.assertEqual(actor.description, test_description)
    
    def test_image(self):
        test_image = 'image.jpg'
        actor = ActorFactory.build(image=test_image)
        self.assertEqual(actor.image, test_image)

    def test_age(self):
        test_age = 35
        actor = ActorFactory.build(age=test_age)
        self.assertEqual(actor.age, test_age)

    def test_str_return(self):
        actor = ActorFactory.build()
        self.assertEqual(actor.__str__() , actor.user.username)


class GenreTestCase(TestCase):

    def test_name(self):
        test_name = 'Horror'
        genre = GenreFactory.build(name=test_name)
        self.assertEqual(genre.name, test_name)
        
    def test_description(self):
        td = 'Test Description'
        genre = GenreFactory.build(description=td)
        self.assertEqual(genre.description, td )
        
    def test_slug(self):
        test_name = 'TestSlug'
        test_slug = slugify(test_name)
        genre = GenreFactory.build(name=test_name, slug=test_slug)
        self.assertEqual(genre.slug, test_slug)
        
    def test_str_return(self):
        genre = GenreFactory.build()
        self.assertEqual(genre.__str__(), genre.name)


class ViewerTestCase(TestCase):
    def test_ip(self):
        test_ip = '127.0.0.1'
        viewer = ViewerFactory.build(ip=test_ip)
        self.assertEqual(viewer.ip, test_ip)

    def test_user(self):
        test_user = UserFactory()
        viewer = ViewerFactory.build(user=test_user)
        self.assertEqual(viewer.user, test_user)

    def test_response(self):
        client = Client()
        test_user = UserFactory()
        time = datetime.datetime.now()
        viewer = ViewerFactory.build(id=1, user=test_user, viewed_on=time, ip='2.2.2.2')
        response = client.get("", {'id':1}, {'ip': '2.2.2.2', 'user_id':1, 'viewed_on':time})
        self.assertEqual(response.status_code, 200)


class ArticleTestCase(TestCase):

    def test_article(self):
        self.client = Client()
        # article = ArticleFactory.create(viewers=(viewer1, viewer2, viewer3))
        # pp.pprint(article.__dict__)

        # video_mock = MagicMock(spec=File)
        # video_mock.name = 'video.mp4'

        # user_article= UserFactory.build(username='articleuser')
        # user_view = UserFactory.build(username='vuser')
        # user_voice = UserFactory.build(username='voicer1')
        # user_time = UserFactory.build(username='timer1')
        # user_sub = UserFactory.build(username='sub1')

        # voicer = ActorFactory.build(user=user_voice)                                        #
        # timer = ActorFactory.build(user=user_time)                                        #
        # sub = ActorFactory.build(user=user_sub)
        # genre = GenreFactory.build()           
        # video= VideoFactory.build()

        # article.viewers.add(viewer)
        # article.voicing.add(voicer)
        # article.timing.add(timer)
        # article.subtitles.add(sub)
        # article.genres.add(genre)
        # article.videos.add(video)

        # review = ReviewFactory.build(article=article, author=user_article, text='Text review')
        # review2 = ReviewFactory.build(article=article, author=user_voice, text='Text review2', parent=review)
        # print(article)
        # print(article.viewers)



    # def test_link_slug(self):
    #     article = .objects.get(title='Test Title')
    #     self.assertEqual(article.link, 'testus-titlus')

    # def test_on_main(self):
    #     article = Article.objects.get(link='testus-titlus')
    #     self.assertEqual(article.on_main, True)

    # def test_get_response(self):
    #     response = self.client.get('')
    #     self.assertEqual(response.status_code, 200)
    
    # def test_count(self):
    #     response = self.client.get('', {'season': 'Winter-2022'}, {'county': 'Япония'})
    #     self.assertEqual(response.status_code, 200)

    # def test_m2m_response(self):
    #     response = self.client.get('', 
    #         {'genres': 1},
    #         {'viewers': 1},
    #         {'voicing': 1},
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_m2m_response2(self):
    #     response = self.client.get('', 
    #         {'timing': 1},
    #         {'subtitles': 1},
    #         {'videos': 1}
    #     )
    #     self.assertEqual(response.status_code, 200)

    # def test_get_absolute_url(self):
    #     article = Article.objects.get(title_alt='Testus Titlus')
    #     self.assertEqual(article.get_absolute_url(), '/articles/testus-titlus/')

    # def test_get_reviews(self):
    #     article = Article.objects.get(title_alt='Testus Titlus')
    #     author = article.author.id
    #     reviews_list = article.reviews.all()
    #     review = reviews_list[0]
        
    #     self.assertEqual(review.article, article)
    #     self.assertEqual(review.author, author)
    #     self.assertEqual(review.text, 'Text review')
        
    #     self.assertEqual(len(reviews_list), 2)

class ArticleShotTestCase(TestCase):

    def test_str_return(self):
        articleshot = ArticleShotFactory.build(title='Test Title')
        print(articleshot.__str__(), articleshot.title)
        self.assertEqual(articleshot.__str__() , articleshot.title)


#TODO:Сделать тест дерева
class ReviewTestCase(TestCase):
    def test_reviews(self):
        review = ReviewFactory.build(id=1)
        self.assertEqual(review.__str__(), f'{review.author}:{review.text}')


class VideoTestCase(TestCase):
    def test_video(self):
        test_id = 1
        test_article = ArticleFactory.build()
        video = VideoFactory.build(id=test_id, article=test_article, file=video_mock.name)
        # self.assertEqual(video.__str__(), (f"{video.article}-{video.episode}-{video.title}",))