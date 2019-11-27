from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(ugettext_lazy('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=9)
    ddd = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
