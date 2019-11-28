from django.db import models
from users.models import User
from pieces.models import Piece

STATUSES = (
    (0, "Opened"),
    (1, "Finnished")
)

class Demand(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="demands")
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name="demands")
    street = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    number = models.IntegerField()
    postal_code = models.CharField(max_length=9)
    status = models.IntegerField(default=0, choices= STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def contact(self):
        if not self.owner.is_staff:
            return {'phone': self.owner.profile.phone,
                    'email': self.owner.email}

    def piece_description(self):
        return {'description': self.piece.description}

    def address(self):
        return {'street': self.street,
                'neighborhood': self.neighborhood,
                'city': self.city,
                'state': self.state,
                'number': self.number,
                'postal_code': self.postal_code
                }