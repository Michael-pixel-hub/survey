from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from .tasks import agent_send_mail


@receiver(post_save, sender=Order)
def save_order(sender, instance, created, **kwargs):

    if created:
        agent_send_mail.apply_async((instance.id, ), countdown=120)
