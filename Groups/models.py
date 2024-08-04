from django.db import models
from Authentications.models import User

class Group(models.Model):
    group_name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name='group_members', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class JoinLink(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)
    
