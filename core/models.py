from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField

from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session 

ITEM_CATEGORY = (
        ('Short wear', 'Short wear'),
        ('Normal wear', 'Normal wear'),
        ('Long wear', 'Long wear')
    )

LABEL_CATEGORY = (
        ('P', 'primary'),
        ('S', 'secondary'),
        ('D', 'danger')
    )



class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.FloatField()
    item_category = models.CharField(max_length=30, choices=ITEM_CATEGORY)
    label = models.CharField(max_length=1, choices=LABEL_CATEGORY, default='P')
    description = models.CharField(max_length=250, help_text='250 words max')
    discount_price = models.FloatField( blank=True, null=True)
    slug = models.SlugField(blank=True)
  
    def __str__(self):
        return self.name

    def absolute_url(self):
        return reverse('')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    is_ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1),])

    def __str__(self):
        return self.item.name

    def get_item_price(self):
        return self.quantity * self.item.price
    
    def get_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_savings(self):
        return self.get_item_price() - self.get_item_discount_price()


    def get_total_price(self):
        if self.item.discount_price:
            return self.get_item_discount_price()
        return self.get_item_price()


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    street_address = models.CharField(max_length=150)
    apartment_address = models.CharField(max_length=100, blank=True)
    country = CountryField(blank_label='(select country)')
    zip = models.CharField(max_length=50)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Order(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='First Name')
    last_name = models.CharField(max_length=50, verbose_name='Last Name')
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    is_ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True,)
    

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
        
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total
