from rest_framework import serializers

from filetransfer.serializers.user import UserSerializer
from filetransfer.models.file import File

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "file",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        organization = user.organization

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

