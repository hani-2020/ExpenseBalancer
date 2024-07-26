from django.db import models
from Authentications.models import User

class FriendRequests(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='from_requests', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_user', 'to_user')