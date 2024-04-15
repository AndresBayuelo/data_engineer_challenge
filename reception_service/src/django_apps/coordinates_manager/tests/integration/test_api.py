import csv
import io
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from src.django_apps.coordinates_manager.models import File, Coordinate


class FileUploadViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("upload-csv")

        # Generar un archivo CSV válido en memoria
        csv_output = io.StringIO()
        fieldnames = ['lat', 'lon']
        writer = csv.DictWriter(
            csv_output, fieldnames=fieldnames, delimiter='|'
        )
        writer.writeheader()
        writer.writerow({'lat': "''52,923454''", 'lon': "''-1,474217''"})
        writer.writerow({'lat': "''53,457321''", 'lon': "''-2,262773''"})
        writer.writerow({'lat': "''50,871446''", 'lon': "''-0,729985''"})
        writer.writerow({'lat': "''50,215687''", 'lon': "''-5,191573''"})
        writer.writerow({'lat': "''57,540178''", 'lon': "''-3,758607''"})
        writer.writerow({'lat': "''nan''", 'lon': "''nan''"})

        # Convertir a bytes
        self.csv_bytes = io.BytesIO(csv_output.getvalue().encode())

    def test_upload_valid_csv(self):
        # print(self.csv_bytes.getvalue().decode())
        file_upload = SimpleUploadedFile(
            "valid_coordinates.csv", self.csv_bytes.getvalue()
        )
        data = {'file': file_upload}

        response = self.client.post(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'OK')

        # Verificar que se haya creado un nuevo registro en la tabla File
        file = File.objects.last()
        self.assertIsNotNone(file)
        self.assertEqual(file.name, "valid_coordinates.csv")

        # Verificar que se hayan creado los registros en la tabla Coordinate
        coordinates = Coordinate.objects.filter(file_id=file.id)
        # Deberían haberse creado 5 registros
        self.assertEqual(len(coordinates), 5)


class FileDetailViewTestCase(APITestCase):
    def setUp(self):
        self.file = File.objects.create(name="Test file", status="in_process")
        Coordinate.objects.create(
            latitude=12.345,
            longitude=23.456,
            file=self.file,
            postal_code="12345",
        )
        Coordinate.objects.create(
            latitude=34.567,
            longitude=45.678,
            file=self.file
        )

    def test_get_file_detail(self):
        url = f'/api/coordinates-manager/file-detail/?file_id={self.file.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "file_id": self.file.id,
            "name": self.file.name,
            "status": self.file.status,
            "coordinates_processed": 1,
            "coordinates_total": 2
        })
