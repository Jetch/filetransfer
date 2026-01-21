from django.db import models
from django.conf import settings
from filetransfer.models.file import File

class Download(models.Model):
    downloaded_at = models.DateTimeField(auto_now_add=True, db_index = True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, db_index=True, related_name="downloads")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True, related_name="downloads"
        )

    def __str__(self):
        return f"{self.user.username} downloaded {self.file.filename}"
