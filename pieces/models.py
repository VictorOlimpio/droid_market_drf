from django.db import models

TYPES = (
    ("arm", "Arm"),
    ("leg", "Leg"),
    ("body", "Body"),
    ("head", "Head"),
    ("blaster", "Blaster"),
    ("shield", "Shield")
)


class Piece(models.Model):
    type = models.CharField(max_length=15, choices= TYPES)
    description = models.TextField(max_length=400)
    value = models.FloatField()
