from django.db import models
from user.models import CustomUser


class UserCart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"This Cart is for {self.user.email}"
