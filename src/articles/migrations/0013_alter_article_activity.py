# Generated by Django 4.2 on 2023-05-31 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_article_on_main'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='activity',
            field=models.CharField(choices=[('Продолжается', 'Продолжается'), ('Завершён', 'Завершён')], default='Продолжается', verbose_name='Статус'),
        ),
    ]
