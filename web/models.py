from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserData(models.Model):
    GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ('prefer_not_to_say', 'Prefer not to say'),
    ]
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    phone = models.CharField(max_length=14)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
