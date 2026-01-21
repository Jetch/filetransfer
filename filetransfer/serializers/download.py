from rest_framework import serializers

from filetransfer.models.download import Download

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
