from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='',null=False, blank=True)
    name = models.CharField(max_length=100)
   

    def __str__(self):
        return f"{self.category.name} → {self.name}"
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='',null=False, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,default='',null=False, blank=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # is_available = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name