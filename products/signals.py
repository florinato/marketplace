from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Report


@receiver(post_save, sender=Report)
def update_product_on_report_status_change(sender, instance, **kwargs):
    if instance.status == 'resolved':
        instance.product.is_blocked = True
        instance.product.save()
