from django.db import models
from django.contrib.auth.models import AbstractUser
from filetransfer.models.organization import Organization

class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return f"{self.username} ({self.organization.name})"
