from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male', 'male'),
        ('female', 'female'),
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nick_name = models.CharField('nick_name', max_length=50, blank=True, default='')
    birthday = models.DateField('birthday', null=True, blank=True)
    gender = models.CharField('sex', max_length=6, choices=USER_GENDER_TYPE, default='male')
    address = models.CharField('address', max_length=100, blank=True, default='')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100,
                              verbose_name='avatar')
    description = models.TextField('introduction', max_length=200, default='')
    signature = models.CharField('signature', max_length=100, default='')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username


class EmailVerifyRecord(models.Model):

    SEND_TYPE_CHOICES = (
        ('register', 'register'),
        ('forget', "forgot password"),
    )

    code = models.CharField("verification code", max_length=20)
    email = models.EmailField('email', max_length=35)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, max_length=20, default='register')
    send_time = models.DateTimeField('time', default=timezone.now().strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        verbose_name = "Email verification code"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


