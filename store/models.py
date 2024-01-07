from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


# Product Filtering
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


# Categories Table
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    icon = models.FileField(upload_to='icons/')
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name
    
# Product Table
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_stock = models.PositiveIntegerField(validators=[MaxValueValidator(500)], default=0)
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()
    days_in_stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def formatted_price(self):
        return '{:,.2f}'.format(self.price)

    def __str__(self):
        return f'{self.name} - Price: {self.formatted_price()}'
    
    def discounted_price(self):
        discount_percentage = Decimal(self.discount) / 100
        discounted_price = self.price * (1 - discount_percentage)
        
        formatted_price = '{:,.2f}'.format(discounted_price)
        
        return formatted_price


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.created:
            self.days_in_stock = (timezone.now() - self.created).days
        super(Product, self).save(*args, **kwargs)

def update_days_in_stock(sender, instance, **kwargs):
    if instance.created and instance.is_active:
        instance.days_in_stock = (timezone.now() - instance.created).days
    else:
        instance.days_in_stock = 0

pre_save.connect(update_days_in_stock, sender=Product)