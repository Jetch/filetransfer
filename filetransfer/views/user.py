from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from filetransfer.models.download import Download
from filetransfer.serializers.user import UserDownloadSerializer


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
