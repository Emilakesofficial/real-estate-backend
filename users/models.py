from datetime import timedelta 
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import string
from django.utils.crypto import get_random_string
    
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    currency_code = models.CharField(max_length=10, default='NGN')
    currency_symbol = models.CharField(max_length=5, default='#')
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    ROLE_CHOICES = (
        ('agent', 'Agent'),
        ('renter/buyer', 'Renter/Buyer'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.role}"


def generate_token():
    return get_random_string(length=6, allowed_chars=string.digits + string.ascii_uppercase)

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, default=generate_token, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() - self.created_at < timedelta(minutes=15)

    def __str__(self):
        return f"Token for {self.user.email}"
    
class PasswordOTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    
    def is_valid(self, otp):
        return self.otp == otp and timezone.now() < self.expires_at
    
    def __str__(self):
        return f'OPT for {self.user.email} - Expires at {self.expires_at}'

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class Passcode(models.Model):
    passcode = models.CharField(max_length=6)



