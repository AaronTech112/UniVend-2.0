from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    
    # Adding profile fields directly to the user model
    campus = models.ForeignKey('Campus', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'campus']  # Making campus required during signup

    def __str__(self):
        return f"{self.username} - {self.email}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        


class Campus(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.name} - {self.campus.name}"

class KYC(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=20, unique=True)
    school_id_photo = models.ImageField(upload_to='kyc/school_ids/')
    passport_photo = models.ImageField(upload_to='kyc/passports/')
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"KYC for {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

class Review(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username}"

class Service(models.Model):
    provider = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    delivery_time = models.PositiveIntegerField(help_text="Delivery time in days")
    
    def __str__(self):
        return self.title

class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    is_primary = models.BooleanField(default=False)

class Cart(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Conversation(models.Model):
    participants = models.ManyToManyField('CustomUser', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

# class UserProfile(models.Model):
#     user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
#     campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True)
#     department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
#     bio = models.TextField(blank=True)
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"Profile for {self.user.username}"