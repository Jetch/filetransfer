from django.db.models import Count

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from filetransfer.models.download import Download
from filetransfer.models.file import File
from filetransfer.serializers.download import FileDownloadSerializer
from filetransfer.serializers.file import FileUploadSerializer, FileListSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_file(request):
    serializer = FileUploadSerializer(
        data=request.data,
        context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = (
        File.objects
        .select_related("uploaded_by", "organization")
        .annotate(download_count=Count("downloads"))
        .order_by("-uploaded_at")
    )

    serializer = FileListSerializer(files, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def file_downloads(request, file_id):
    downloads = (
        Download.objects
        .filter(file_id=file_id)
        .select_related("user")
        .order_by("-downloaded_at")
    )

    serializer = FileDownloadSerializer(downloads, many=True)
    return Response(serializer.data)