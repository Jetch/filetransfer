from django.urls import path

from filetransfer.views.download import download_file
from filetransfer.views.file import upload_file, file_downloads, list_files
from filetransfer.views.organization import list_organizations
from filetransfer.views.user import user_downloads

urlpatterns = [
    path("files/", list_files, name="list-files"),
    path("files/upload/", upload_file, name="upload-file"),
    path("files/<int:file_id>/download/", download_file, name="download-file"),
    path("files/<int:file_id>/downloads/", file_downloads, name="file-downloads"),
    path("organizations/", list_organizations, name="list-organizations"),
    path("users/<int:user_id>/downloads/", user_downloads, name="user-downloads"),
]