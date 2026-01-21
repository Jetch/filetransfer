from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from filetransfer.models.download import Download
from filetransfer.models.file import File


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    """
    Downloads a file.
    """
    file_obj = get_object_or_404(File, id=file_id)

    Download.objects.create(
        file=file_obj,
        user=request.user
    )

    return FileResponse(
        file_obj.file.open("rb"),
        as_attachment=True,
        filename=file_obj.filename
    )
