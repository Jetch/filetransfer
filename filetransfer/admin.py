from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, File, Download

admin.site.register(User, UserAdmin)
admin.site.register(Organization)
admin.site.register(File)
admin.site.register(Download)
# Register your models here.
