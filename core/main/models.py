from django.db import models
from django.conf import settings


# Create your models here.


class UserId(models.Model):
    userid = models.BigIntegerField(null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
