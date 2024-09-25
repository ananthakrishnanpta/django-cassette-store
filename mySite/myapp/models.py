from django.db import models
from django.utils.timezone import get_current_timezone
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100) # becomes varchar
    price = models.PositiveIntegerField() # becomes unsigned int
    description = models.TextField() # becomes long or medium text
    stock = models.PositiveIntegerField(default=1)
    created_at =  models.DateTimeField(auto_now_add=True) # stores the curdatetime() in a datetime field
    pic = models.ImageField(upload_to="products/", null = True)
    def __str__(self):
        return self.name