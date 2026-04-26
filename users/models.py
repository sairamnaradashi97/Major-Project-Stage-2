from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Interaction(models.Model):
    COUPON_LEVEL_CHOICES = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    QUANTITY_DISCOUNT_CHOICES = [
        ('None', 'None'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    DEVICE_CHOICES = [
        ('Desktop', 'Desktop'),
        ('Mobile', 'Mobile'),
        ('Tablet', 'Tablet'),
    ]

    TIME_OF_DAY_CHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coupon_discount_level = models.CharField(max_length=10, choices=COUPON_LEVEL_CHOICES)
    quantity_discount_level = models.CharField(max_length=10, choices=QUANTITY_DISCOUNT_CHOICES)
    added_to_cart = models.BooleanField(default=False)
    time_of_interaction = models.CharField(max_length=10, choices=TIME_OF_DAY_CHOICES)
    device = models.CharField(max_length=10, choices=DEVICE_CHOICES)
    purchased = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# Create your models here.




from django.db import models

class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=10)  # Adjusted max_length to 10 for mobile numbers
    email = models.EmailField(unique=True, max_length=100)  # Use EmailField for better validation
    locality = models.CharField(max_length=100)
    address = models.TextField(max_length=1000)  # Use TextField for longer addresses
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='waiting')

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'user_registrations'

