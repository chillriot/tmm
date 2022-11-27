import email
from statistics import mode
from django.db import models

# Create your models here.
class UserMails(models.Model):
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    external_id = models.IntegerField(null=True, blank=True)

