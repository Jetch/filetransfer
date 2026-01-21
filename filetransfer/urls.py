from django.urls import path

from filetransfer.views.file import file_download, file_downloads, file_list
from filetransfer.views.organization import organization_list
from filetransfer.views.user import user_downloads

urlpatterns = [
    path("files/", file_list, name="file-list"),
    path("files/<int:file_id>/download/", file_download, name="file-download"),
    path("files/<int:file_id>/downloads/", file_downloads, name="file-downloads"),
    path("organizations/", organization_list, name="organization-list"),
    path("users/<int:user_id>/downloads/", user_downloads, name="user-downloads"),
]
