from django.db.models import Count

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from filetransfer.models.organization import Organization
from filetransfer.serializers.organization import OrganizationSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_organizations(request):
    """
    Lists all organization with download count.
    """
    organizations = (
        Organization.objects
        .annotate(total_downloads=Count("files__downloads"))
        .order_by("name")
    )

    serializer = OrganizationSerializer(organizations, many=True)
    return Response(serializer.data)
