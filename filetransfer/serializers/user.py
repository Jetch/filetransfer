from rest_framework import serializers

from ..models.download import Download
from ..models.user import User

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="user.organization.name",
        read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "organization"]


class UserDownloadSerializer(serializers.ModelSerializer):
    file = serializers.CharField(
        source="file.file",
        read_only=True
    )
    filename = serializers.CharField(
        source="file.filename",
        read_only=True
    )
    

    class Meta:
        model = Download
        fields = [
            "id",
            "file",
            "filename",
            "downloaded_at",
        ]