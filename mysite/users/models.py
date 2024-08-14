from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', 'male'),
        ('female', 'female'),
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nike_name = models.CharField('nick_name', max_length=50, blank=True, default='')
    birthday = models.DateField('birthday', null=True, blank=True)
    gender = models.CharField('sex', max_length=6, choices=USER_GENDER_TYPE, default='male')
    address = models.CharField('address', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100,
                              verbose_name='avatar')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username





