from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.BooleanField(default=False)  
    in_stock = models.BooleanField(default=True) 
    image = models.ImageField(upload_to='media/', null=True, blank=True)  
    rating = models.DecimalField(
    max_digits=3,
    decimal_places=1,
    default=0.0,
    validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
)   

    def __str__(self):
        return self.name
    
    
class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_ratings')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user') 

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} - {self.rating}"


class productimage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='media/')

@receiver([post_save, post_delete], sender=ProductRating)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    avg = product.ratings.aggregate(average=Avg('rating'))['average']
    product.rating = avg or 0
    product.save(update_fields=['rating'])

    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity