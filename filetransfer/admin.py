from django.contrib import admin
from .models.user import User
from .models.organization import Organization
from .models.file import File
from .models.download import Download

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(File)
admin.site.register(Download)
# Register your models here.
