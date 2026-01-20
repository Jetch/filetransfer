from django.urls import path
from . import views

urlpatterns = [
    path("files/upload/", views.upload_file, name="upload-file"),
    path("files/", views.list_files, name="list-files"),
    path("files/<int:file_id>/download/", views.download_file, name="download-file"),
    path("files/<int:file_id>/downloads/", views.file_downloads, name="file-downloads"),
    path("organizations/", views.list_organizations, name="list-organizations"),
    path("users/<int:user_id>/downloads/", views.user_downloads, name="user-downloads"),
]