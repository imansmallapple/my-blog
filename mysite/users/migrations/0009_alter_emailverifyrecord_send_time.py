# Generated by Django 5.1 on 2024-09-10 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_pendinguser_alter_emailverifyrecord_send_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default='2024-09-10 22:10:16', verbose_name='time'),
        ),
    ]
