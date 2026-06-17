from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
