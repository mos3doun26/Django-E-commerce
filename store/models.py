from django.db import models
from django.contrib.auth.models import User
import datetime
from PIL import Image
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    address_1 = models.CharField(max_length=50, blank=True)
    address_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)
    old_cart = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)

class Category(models.Model):
    name = models.CharField(max_length=50)
    # products = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=200, default="", null=True, blank=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to="uploads/product/", null=True, blank=True)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default= 0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img = img.resize((450, 300))
        img.save(self.image.path)
    

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=100)
    # username = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default="", blank=True, null=True)
    quantity = models.IntegerField(default=1 )
    phone = models.CharField(max_length=12, default="", blank=True, null=True)
    date = models.DateField(default=datetime.datetime.today)
    status =  models.BooleanField(default=False)

    def __str__(self):
        return self.product.name
