from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    unit = models.CharField(max_length=20, default='kg')

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True)  # optional or required
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # --- ADD THIS NEW FIELD ---
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class CompostExchange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    compost_amount = models.FloatField()
    credits_earned = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.compost_amount}kg - {self.credits_earned} credits"

