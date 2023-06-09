# Generated by Django 4.2 on 2023-05-29 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_rename_user_review_author_alter_review_article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'verbose_name': 'Актёр', 'verbose_name_plural': 'Актёры'},
        ),
        migrations.AlterModelOptions(
            name='viewer',
            options={'verbose_name': 'Посетитель', 'verbose_name_plural': 'Посетители'},
        ),
        migrations.RemoveField(
            model_name='video',
            name='description',
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
    ]
