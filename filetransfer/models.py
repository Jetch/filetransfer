from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Organization(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.username} ({self.organization.name})"


class File(models.Model):
    file = models.FileField(upload_to="files/")
    filename = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="uploaded_files")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="files")

    def __str__(self):
        return self.filename


class Download(models.Model):
    downloaded_at = models.DateTimeField(auto_now_add=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="downloads")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="downloads")

    def __str__(self):
        return f"{self.user.username} downloaded {self.file.filename}"