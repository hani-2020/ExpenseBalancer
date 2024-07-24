from django.db import models
from Authentications.models import User

class Group(models.Model):
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name='group_members', blank=True)
