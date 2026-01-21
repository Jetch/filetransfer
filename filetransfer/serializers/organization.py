from rest_framework import serializers

from ..models.organization import Organization

class OrganizationSerializer(serializers.ModelSerializer):
    total_downloads = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "total_downloads"]

