from datetime import datetime, timedelta
from pathlib import Path
from typing import IO, Generator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Video, Article, Viewer
from src.profiles.models import UserNet
from django.core.exceptions import FieldError, ObjectDoesNotExist

def ranged(
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()

def open_file(request, pk, episode: int) -> tuple:
    _video = get_object_or_404(Video.objects.filter(article_id=pk).filter(episode=episode))

    path = Path(_video.file.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        content_ranges = content_range.strip().lower().split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        content_range = f"bytes {range_start}-{range_end}/{file_size}"
    
    return file, status_code, content_length, content_range


def check_date():
    # print(Viewer.objects.all().values('viewed_on'))
    curent_date = datetime.today()
    start_date = curent_date - timedelta(days=5)
    queryset = Article.objects.filter(viewers__viewed_on__range=[start_date, curent_date]).values('viewers').order_by('-viewers')[:5]
    print(queryset)

#TODO: Добавить уведомления в результате функции
def check_article_user(self, request, **kwargs):
    """Проверка подписки и рекомендаций"""
    
    article = self.kwargs.get('article')
    user_pk = self.kwargs.get('user')
    url = request.META.get('HTTP_REFERER')
    try :
        self.model.objects.get(article_id=article, users=user_pk)
    except ObjectDoesNotExist:
        self.model.objects.create(article_id=article).users.add(user_pk)  
    finally:
        return url