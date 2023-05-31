# Generated by Django 4.2 on 2023-05-28 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0004_viewer_viewed_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='name',
        ),
        migrations.AddField(
            model_name='actor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Актёр'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='image',
            field=models.ImageField(blank=True, upload_to='actors/', verbose_name='Изображение'),
        ),
    ]