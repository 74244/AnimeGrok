from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View, CreateView


from src.base.mixins import CountViewerMixin
from src.articles.forms import RatingForm, ReviewForm
from src.articles.models import Article, Rating,  Genre, Review

class GenreAll:
    """ Жанры """

    def get_genres(self):
        return Genre.objects.all()

class HomeView(ListView):
    model = Article
    template_name = "home.html"

    
class ArticleListView(GenreAll, ListView):
    """Список аниме"""
    
    template_name = "articles/article-list.html"
    paginate_by = 12
    
    def get_queryset(self) -> QuerySet[Any]:
        return Article.objects.all().prefetch_related('viewers', 'genres', 'article_episodes').only('title', 'link', 'genres', 'viewers', 'season', 'series', 'poster')
    

class ArticleDetailView(DetailView, CountViewerMixin, Genre):
    """Полное описание аниме"""

    # model = Article
    template_name = "articles/article-details.html"
    slug_field = 'link'
    context_object_name = 'article'
    queryset = Article.objects.all().select_related('user', 'category').prefetch_related('viewers', 'genres', 'article_episodes', 'reviews', 'ratings', 'voicing', 'timing', 'subtitles')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm
        context['ip'] = self.get_mixin_ip(self.request)

        return context

class AddRatingStar(View, CountViewerMixin):
    """Добавление рейтинга к аниме"""
    
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                
                article_id=int(request.POST.get('article')),
                defaults={'star_id':int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


#TODO: доделать форму после реализации аутентификации
#FIXME: Исправить вёрстку отзывов в виде дерева

class ReviewCreateView(CreateView):
    """Добавление отзыва"""
    model = Review
    form_class = ReviewForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_valid(self, form):
        review = form.save(commit=False)
        review.article_id = self.kwargs.get('pk')
        if self.request.user.is_authenticated:
            review.author = self.request.user
        # else:
        #     review.author = form.cleaned_data.get('user')
        review.parent_id = form.cleaned_data.get('parent')
        review.save()

        if self.is_ajax():
            if self.request.user.is_authenticated:
                data = {
                    'is_child': review.is_child_node(),
                    'id': review.id,
                    'author': review.author,
                    'parent_id': review.parent_id,
                    'create_at': review.create_at.strftime('%Y-%b-%d %H:%M:%S'),
                    'text': review.text,
                    'get_absolute_url': review.article.get_absolute_url()
                }
            return JsonResponse(data, status=200)
        return redirect(review.article.get_absolute_url())
                

class Search(ListView):
    """Поиск Аниме"""

    template_name = "articles/article-list.html"
    paginate_by = 9

    def get_queryset(self):
        return Article.objects.filter(title__icontains=self.request.GET.get("q"))
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get("q")
        return context


# #TODO: JS DOM
class TopViewsFilterView(ListView):
    pass
#     """Фильтр аниме в json"""

#     def get_queryset(self):
#         queryset = Article.objects.all()[:5].values('title', 'poster', 'viewers',)
#         return queryset

#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         return JsonResponse({'top_v_articles':list(queryset)})
