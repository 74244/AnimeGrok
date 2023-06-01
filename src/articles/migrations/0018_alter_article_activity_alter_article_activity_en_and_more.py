# Generated by Django 4.2 on 2023-06-01 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_alter_video_options_article_activity_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='activity',
            field=models.CharField(choices=[('Продолжается', 'Продолжается'), ('Завершён', 'Завершён'), ('Airling', 'Airling'), ('Completed', 'Completed')], default='Продолжается', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='article',
            name='activity_en',
            field=models.CharField(choices=[('Продолжается', 'Продолжается'), ('Завершён', 'Завершён'), ('Airling', 'Airling'), ('Completed', 'Completed')], default='Продолжается', null=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='article',
            name='activity_ru',
            field=models.CharField(choices=[('Продолжается', 'Продолжается'), ('Завершён', 'Завершён'), ('Airling', 'Airling'), ('Completed', 'Completed')], default='Продолжается', null=True, verbose_name='Статус'),
        ),
    ]
