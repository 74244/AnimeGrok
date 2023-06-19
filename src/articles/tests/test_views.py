from django.test import Client, TestCase
from django.urls import reverse

from src.articles.models import Article
from src.articles.tests.factories import ArticleFactory

'assertEqual'

class ArticlesViewTestCase(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)

    def test_articles_list(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)

    def test_articles_detail(self):
        article = ArticleFactory.build(link='mashle')
        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 302)     #Редирект на EN или RU версию страницы