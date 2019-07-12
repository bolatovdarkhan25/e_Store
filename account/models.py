from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, default='', verbose_name='Город')
    phone = models.CharField(max_length=255, default='', verbose_name='Номер телефона')
    patronymic = models.CharField(max_length=255, default='', verbose_name='Отчество')

    def __str__(self):
        return self.user.username
