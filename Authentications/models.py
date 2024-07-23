from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    
    def get_by_natural_key(self, email):
        return self.get(email=email)

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='friendsfield', blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
