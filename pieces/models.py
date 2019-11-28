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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
