# Generated by Django 4.2 on 2023-05-28 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_alter_article_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Название'),
        ),
    ]
