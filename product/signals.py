from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Product, Review

@receiver(post_save, sender=Review)
def update_product_rating_on_save(sender, instance, **kwargs):
    instance.product.update_rating()


@receiver(post_delete, sender=Review)
def delete_product_rating_on_save(sender, instance, **kwargs):
    instance.product.update_rating()

