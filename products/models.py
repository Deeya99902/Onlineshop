from django.db import models
from django.contrib.auth.models import User
from django.urls import  reverse
from PIL import Image

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
     name = models.CharField(max_length=200,unique=True)   
     description = models.TextField(blank=True)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     Category = models.ForeignKey(Category, on_delete=models.CASCADE)
     image = models.ImageField(upload_to='products_pics',)
     stock = models.PositiveIntegerField(default=0)
     available = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     seller = models.ForeignKey(User, on_delete=models.CASCADE)
     
     def __str__(self):
        return self.name
    
def get_absolute_url(self):
    return reverse("product_details", kwargs={"pk": self.pk})

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    
    try:
       if self.image and self.image.name != 'products_pics/default.jpg':
           img = Image.open(self.image.path)
           if img.height > 800 or img.width >800:
               output_size = (800,800)
               img.thumbnail(output_size)
               img.save(self.image.path)
               
    except(OSError,IOError):
        pass
               
           
      

    
    
  
    
   
   
