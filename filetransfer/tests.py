from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from filetransfer.models.user import User
from filetransfer.models.organization import Organization
from filetransfer.models.file import File
from filetransfer.models.download import Download

class BaseAPITestCase(APITestCase):
    """Base API test, creating users and login"""
    def setUp(self):
        self.org1 = Organization.objects.create(name="Org One")
        self.org2 = Organization.objects.create(name="Org Two")

        self.user1 = User.objects.create_user(
            username="user1",
            password="password123",
            email="user1@example",
            organization=self.org1
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="password123",
            email="user2@example",
            organization=self.org2
        )

        self.client.login(username="user1", password="password123")

class UploadFileTests(BaseAPITestCase):
    """Tests for file upload"""
    def test_upload_file(self):
        """Testing simple txt file upload"""
        url = reverse("upload-file")

        uploaded_file = SimpleUploadedFile(
            "test.txt",
            b"Hello world",
            content_type="text/plain"
        )

        response = self.client.post(
            url,
            {"file": uploaded_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(File.objects.count(), 1)

        file_obj = File.objects.first()
        self.assertEqual(file_obj.uploaded_by, self.user1)
        self.assertEqual(file_obj.organization, self.org1)
        self.assertEqual(file_obj.filename, "test.txt")

class FileListTests(BaseAPITestCase):
    """Tests for file list"""
    def setUp(self):
        super().setUp()

        self.file = File.objects.create(
            file=SimpleUploadedFile("file.txt", b"data"),
            filename="file.txt",
            uploaded_by=self.user1,
            organization=self.org1,
        )

        Download.objects.create(file=self.file, user=self.user1)
        Download.objects.create(file=self.file, user=self.user2)

    def test_list_files_with_download_count(self):
        """Testing file listing with download count"""
        url = reverse("list-files")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["download_count"], 2)


class DownloadFileTests(BaseAPITestCase):
    """Tests for download file"""
    def setUp(self):
        super().setUp()

        self.file = File.objects.create(
            file=SimpleUploadedFile("download.txt", b"content"),
            filename="download.txt",
            uploaded_by=self.user2,
            organization=self.org2,
        )

    def test_download_creates_record(self):
        """Testing download file and expects record showing it"""
        url = reverse("download-file", args=[self.file.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Download.objects.count(), 1)

        download = Download.objects.first()
        self.assertEqual(download.file, self.file)
        self.assertEqual(download.user, self.user1)

class OrganizationListTests(BaseAPITestCase):
    """Tests for Organization list"""
    def setUp(self):
        super().setUp()

        file1 = File.objects.create(
            file=SimpleUploadedFile("a.txt", b"a"),
            filename="a.txt",
            uploaded_by=self.user1,
            organization=self.org1,
        )

        file2 = File.objects.create(
            file=SimpleUploadedFile("b.txt", b"b"),
            filename="b.txt",
            uploaded_by=self.user1,
            organization=self.org1,
        )

        Download.objects.create(file=file1, user=self.user1)
        Download.objects.create(file=file2, user=self.user2)

    def test_organization_download_count(self):
        """Testing Organization list with download count"""
        url = reverse("list-organizations")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        org_data = next(
            org for org in response.data if org["name"] == "Org One"
        )
        self.assertEqual(org_data["total_downloads"], 2)

class UserDownloadTests(BaseAPITestCase):
    """Tests for user download"""
    def setUp(self):
        super().setUp()

        file1 = File.objects.create(
            file=SimpleUploadedFile("x.txt", b"x"),
            filename="x.txt",
            uploaded_by=self.user2,
            organization=self.org2,
        )

        Download.objects.create(file=file1, user=self.user1)
        Download.objects.create(file=file1, user=self.user2)

    def test_user_downloads(self):
        """Testing for user's downloads"""
        url = reverse("user-downloads", args=[self.user2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class FileDownloadListTests(BaseAPITestCase):
    """Tests for file download list"""
    def setUp(self):
        super().setUp()

        self.file = File.objects.create(
            file=SimpleUploadedFile("shared.txt", b"shared"),
            filename="shared.txt",
            uploaded_by=self.user1,
            organization=self.org1,
        )

        Download.objects.create(file=self.file, user=self.user1)
        Download.objects.create(file=self.file, user=self.user2)

    def test_file_downloads(self):
        """Testing file downloads"""
        url = reverse("file-downloads", args=[self.file.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class AuthenticationTests(APITestCase):
    """Tests for authentication requirement"""
    def test_auth_required_upload_file(self):
        """Testing authentication requirement in file upload"""
        url = reverse("upload-file")

        uploaded_file = SimpleUploadedFile(
            "test.txt",
            b"Hello world",
            content_type="text/plain"
        )

        response = self.client.post(
            url,
            {"file": uploaded_file},
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_list_files(self):
        """Testing authentication requirement in file list"""
        url = reverse("list-files")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_list_organizations(self):
        """Testing authentication requirement in organization list"""
        url = reverse("list-organizations")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_download_file(self):
        """Testing authentication requirement in download file"""
        url = reverse("download-file", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_file_downloads(self):
        """Testing authentication requirement in file downloads"""
        url = reverse("file-downloads", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auth_required_user_downloads(self):
        """Testing authentication requirement in user downloads"""
        url = reverse("user-downloads", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
