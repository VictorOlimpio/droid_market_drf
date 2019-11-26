from django.db import models

class Piece(models.Model):
    type = models.IntegerField()
    description = models.TextField(max_length=400)
    value = models.FloatField()
