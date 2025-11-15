from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    fio = models.TextField(null=True)
    birthday = models.DateField(null=True)
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)

