import datetime
from django.db import models
from Authentications.models import User
from Groups.models import Group

class Expenses(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    split_method = models.IntegerField(
        choices=[(1,'Split equally'),(2,'percentage'),(3,'Custom'),],
        default=1,
    )
