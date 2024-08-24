# Generated by Django 5.1 on 2024-08-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_emailverifyrecord_send_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default='2024-08-24 10:15:14', verbose_name='time'),
        ),
    ]