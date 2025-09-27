from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Avg

class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    campus = models.ForeignKey('Campus', on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    show_phone = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} - {self.email}"

    def get_average_rating(self):
        avg_rating = self.received_reviews.aggregate(Avg('rating'))['rating__avg']
        return avg_rating or 0.0

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_product = models.BooleanField(default=True)  # True for products, False for services
    icon = models.CharField(max_length=50, blank=True)  # Material Icons name

    def __str__(self):
        return self.name

class Listing(models.Model):
    LISTING_TYPE_CHOICES = [
        ('product', 'Product'),
        ('service', 'Service'),
    ]
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, default='product')
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like-new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('negotiable', 'Negotiable'),
        ('hourly', 'Per Hour'),
        ('free', 'Free'),
    ]
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='fixed')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True)
    description = models.TextField(max_length=1000)
    tags = models.CharField(max_length=255, blank=True)  # Comma-separated tags
    location = models.CharField(max_length=255)
    meeting_preferences = models.CharField(max_length=100, blank=True)
    availability = models.TextField(blank=True)  # JSON or text for days/times
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    saves = models.ManyToManyField(CustomUser, related_name='saved_listings', blank=True)

    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listing_images/')
    is_cover = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.listing.title}"

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True)  # Changed to null=True
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.sent_at}"

class Review(models.Model):
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_reviews')
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField()  # 1 to 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.reviewed}"

class Transaction(models.Model):
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sales')
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')

    def __str__(self):
        return f"Transaction for {self.listing} by {self.buyer}"
    

class KYC(models.Model):
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='kyc')
    student_id = models.ImageField(upload_to='student_ids/', blank=True, null=True)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default='pending')
    interests = models.ManyToManyField(Category, blank=True, related_name='kyc_interests')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYC for {self.user.username} ({self.verification_status})"