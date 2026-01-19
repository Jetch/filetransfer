from rest_framework import serializers
from filetransfer.models import Organization, User, File, Download


class OrganizationSerializer(serializers.ModelSerializer):
    total_downloads = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "total_downloads"]

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(
        source="user.organization.name",
        read_only=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "organization"]


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "file",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        organization = user.profile.organization

        return File.objects.create(
            file=validated_data["file"],
            filename=validated_data["file"].name,
            uploaded_by=user,
            organization=organization,
        )

class FileListSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)
    organization = serializers.CharField(
        source="organization.name",
        read_only=True
    )
    download_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = File
        fields = [
            "id",
            "filename",
            "uploaded_by",
            "organization",
            "uploaded_at",
            "download_count",
        ]

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

class FileDownloadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Download
        fields = [
            "id",
            "user",
            "downloaded_at",
        ]