from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.name
