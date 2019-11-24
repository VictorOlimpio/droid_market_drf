from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=9)
    ddd = models.CharField(max_length=4)
    email = models.CharField(max_length=100)
    kind = models.IntegerField(default=0)
