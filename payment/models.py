from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save
import datetime

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_full_name = models.CharField(max_length=200)
    shipping_email = models.CharField(max_length=200)
    shipping_address_1 = models.CharField(max_length=200)
    shipping_address_2 = models.CharField(max_length=200,blank=True, null=True)
    shipping_country = models.CharField(max_length=200)
    shipping_state = models.CharField(max_length=200)
    shipping_city = models.CharField(max_length=200)
    shipping_zip_code = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f"Shipping Address - {self.id}"
    
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_profile = ShippingAddress(user=instance)
        user_profile.save()


post_save.connect(create_shipping, sender=User)
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=3000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(default=datetime.datetime.now, blank=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f"Order - {self.id}"
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Order Item - {self.id}"