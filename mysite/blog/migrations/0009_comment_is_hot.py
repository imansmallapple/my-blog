# Generated by Django 5.1 on 2024-09-12 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_hot',
            field=models.BooleanField(default=False, verbose_name='Is Popular'),
        ),
    ]
