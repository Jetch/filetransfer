from django.contrib import admin
from filetransfer.models.user import User
from filetransfer.models.organization import Organization
from filetransfer.models.file import File
from filetransfer.models.download import Download

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(File)
admin.site.register(Download)
# Register your models here.
