from django.db import models
from django.conf import settings
from filetransfer.models.organization import Organization

class File(models.Model):
    file = models.FileField(upload_to="files/")
    filename = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_files"
        )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, db_index=True, related_name="files")

    def __str__(self):
        return self.filename
