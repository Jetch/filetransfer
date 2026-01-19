from django.db.models import Count
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import File, Organization, Download
from .serializers import (
    FileUploadSerializer,
    FileListSerializer,
    OrganizationSerializer,
    UserDownloadSerializer,
    FileDownloadSerializer,
)


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
def download_file(request, file_id):
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
def list_organizations(request):
    organizations = (
        Organization.objects
        .annotate(total_downloads=Count("files__downloads"))
        .order_by("name")
    )

    serializer = OrganizationSerializer(organizations, many=True)
    return Response(serializer.data)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_downloads(request, user_id):
    downloads = (
        Download.objects
        .filter(user=user_id)
        .select_related("file")
        .order_by("-downloaded_at")
    )

    serializer = UserDownloadSerializer(downloads, many=True)
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