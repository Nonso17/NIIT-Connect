from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    must_change_password = models.BooleanField(default=True)
    profile_completed = models.BooleanField(default=False)

    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
