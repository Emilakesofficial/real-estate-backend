from django.conf import settings
from django.db import models

CATEGORIES = (
    ('SELL', 'For Sale'),
    ('RENT', 'For Rent'),
)

class Property(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties_uploaded')
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties_assigned')
    title = models.CharField(max_length=50)
    property_type = models.CharField(choices=CATEGORIES, max_length=10)
    description = models.TextField(max_length=500)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    location = models.CharField(max_length=300)
    bathroom = models.PositiveIntegerField()
    bedroom = models.PositiveIntegerField()
    main_image = models.ImageField(upload_to='properties/', blank=False, null=False, default='image here')
    image1 = models.ImageField(upload_to='properties/', blank=True, null=True)
    image2 = models.ImageField(upload_to='properties/', blank=True, null=True)
    image3 = models.ImageField(upload_to='properties/', blank=True, null=True)
    image4 = models.ImageField(upload_to='properties/', blank=True, null=True)
    size = models.PositiveIntegerField(help_text="Size in square meters")
    is_published = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def __str__(self):
        return self.agent.first_name

class Enquiry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enquiries')
    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='enquiries')
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Enquiry by {self.user.email} on {self.property.title}"
