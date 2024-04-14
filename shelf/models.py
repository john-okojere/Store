from django.db import models
import uuid
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name

class Sizes(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name

Size = (
    ('Baby Size', 'Baby Size'),
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
    ('X-Large', 'X-Large'),
    ('XX-Large', 'XX-Large'),
    ('XXX-Large', 'XXX-Large')
)

pay = (
    ('Pay on Delivery', 'Pay on Delivery'),
    ('Pay before Delivery', 'Pay before Delivery'),
)

delivery = (
    ('Free Delivery', 'Free Delivery'),
    ('Delivery Fee', 'Delivery Fee'),
)

productType = (
    ('Single Buy', 'Single Buy'),
    ('Min. Buy', 'Min. Buy'),
    ('Gift on Buy', 'Gift on Buy'),
)

class Product(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/%y/%m/%d/')
    categories = models.ManyToManyField(Category)
    size = models.ManyToManyField(Sizes)
    price = models.IntegerField()
    stock = models.IntegerField(verbose_name="number of Available Stock")
    description = models.TextField()
    pay = models.CharField(max_length=25, choices=pay , null=True)
    delivery = models.CharField(choices=delivery, max_length=25, null=True)
    productType = models.CharField(choices=productType, max_length=25, null=True)
    minBuy = models.IntegerField(verbose_name="minBuy", default=1)
    created_date = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return self.name