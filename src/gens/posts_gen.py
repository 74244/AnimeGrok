import random
from djipsum.faker import FakerModel
from django.utils import timezone
from slugify import slugify

from src.gens.data import text_description_ru, data_ru
# from src.gens.genres_gen import genres
from src.profiles.models import UserNet

# users = UserNet.objects.all().values_list('pk', flat=True)
# aut = random.choice(users)
# # generation posts

# for post_number in range(21, 40):
#     slg = data_ru[str(random.randint(1,31))]['title_alt']
#     tagline_gen = text_description_ru[str(random.randint(1,len(text_description_ru)))]
#     text_gen = text_description_ru[str(random.randint(1,len(text_description_ru)))]

#     p = Post.objects.update_or_create(
#         author_id= aut,
#         title=slg,
#         tagline=tagline_gen,
#         text=text_gen,
#         publication_date = timezone.now(),
#         update_date = timezone.now(),
#         url=slugify(slg),
#     )
#     print(post_number)
#     print(p)

# generation genres

# posts = Post.objects.all().count()
# for number in range(posts):
#     upd = Post.objects.get(pk=number+1)
#     genres_cnt = random.randint(1,4)
#     genres_completed = []
#     for i in range(genres_cnt):
#         genre = random.randint(1,32)
#         if genre not in genres_completed:
#             genres_completed.append(genre)
#             upd.tags.add(genre)
#         else:
#             genre = random.randint(1,32)
#             genres_completed.append(genre)
#             upd.tags.add(genre)
    # print(genres_completed)
    # print(i, upd)
# print('end')