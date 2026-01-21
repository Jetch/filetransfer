from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import FileResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from filetransfer.models.download import Download
from filetransfer.models.file import File
from filetransfer.serializers.download import FileDownloadSerializer
from filetransfer.serializers.file import FileUploadSerializer, FileListSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def file_download(request, file_id):
    """
    Downloads a file and creates record of it.
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

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def file_downloads(request, file_id):
    """
    List all downloads of a file.
    """
    downloads = (
        Download.objects
        .filter(file_id=file_id)
        .select_related("user")
        .order_by("-downloaded_at")
    )

    serializer = FileDownloadSerializer(downloads, many=True)
    return Response(serializer.data)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def file_list(request):
    """
    List all files, or create a new file.
    """
    if request.method == "GET":
        files = (
            File.objects
            .select_related("uploaded_by", "organization")
            .annotate(download_count=Count("downloads"))
            .order_by("-uploaded_at")
        )

        serializer = FileListSerializer(files, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = FileUploadSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
