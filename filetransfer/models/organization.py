from django.db import models

class Organization(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name