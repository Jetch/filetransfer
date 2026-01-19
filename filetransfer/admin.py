from django.contrib import admin
from .models import User, Organization, File, Download

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(File)
admin.site.register(Download)
# Register your models here.
