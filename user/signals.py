from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from order.models import UserCart


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        UserCart.objects.create(user=instance)
