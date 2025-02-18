from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class ScholarProfile(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    fields = models.JSONField(default=list)  # Stores array of interests
    works = models.JSONField(default=list)  # Stores work details as JSON

    def __str__(self):
        return self.name if self.name else "Scholar Profile"

class User(AbstractUser):  # Extending Django's built-in User model
    ROLE_CHOICES = [
        ('author', 'Author'),
        ('management', 'Management'),
        ('reviewer', 'Reviewer'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    userID = models.CharField(max_length=10, unique=True, editable=False)
    google_scholar_id = models.CharField(max_length=255, blank=True, null=True)
    emailid = models.EmailField(unique=True, blank=True, null=True)
    scholar_profile = models.OneToOneField(ScholarProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.userID:
            self.userID = f"U{uuid.uuid4().int % 1000000}"  # Generate unique ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# DIFFERENT FOR ALL ROLES
# NO REG. FOR MANAGER
