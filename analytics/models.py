from django.db import models
from products.models import Product


class ClickEventManager(models.Manager):
    def create_event(self, productInstance):
        if isinstance(productInstance, Product):
            obj, created = self.get_or_create(product_hit=productInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ClickEvent(models.Model):
    product_hit = models.OneToOneField(Product)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)
