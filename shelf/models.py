from django.db import models
import uuid
from user.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name

Sizes = (
    ('Baby Size', 'Baby Size'),
    ('Small', 'Small'),
    ('Medium', 'Medium'),
    ('Large', 'Large'),
    ('X-Large', 'X-Large'),
    ('XX-Large', 'XX-Large'),
    ('XXX-Large', 'XXX-Large')
)

class Product(models.Model):
    uid = models.UUIDField( default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product/%y/%m/%d/')
    categories = models.ManyToManyField(Category)
    size = models.CharField(choices=Sizes, max_length=255)
    price = models.IntegerField()
    stock = models.IntegerField(verbose_name="number of Stock")
    description = models.TextField()
    created_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name