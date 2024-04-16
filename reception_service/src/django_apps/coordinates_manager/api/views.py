import io
import os
import requests
import threading

import pandas as pd
from django.db import models
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from src.django_apps.coordinates_manager.api.serializers import (
    CSVUploadSerializer, FileIdSerializer)
from src.django_apps.coordinates_manager.models import Coordinate, File


# Create your views here.
class FileUploadView(APIView):
    parser_class = (FileUploadParser,)
    serializer_class = CSVUploadSerializer

    def _async_get(self, url):
        requests.get(url)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data["file"]
            data_set = csv_file.read().decode("UTF-8")
            # Eliminar comillas adicionales
            data_set = data_set.replace("''", "'")
            io_string = io.StringIO(data_set)
            df = pd.read_csv(io_string, delimiter="|", quotechar="'")

            # Verificar las columnas
            if sorted(df.columns.tolist()) != sorted(["lat", "lon"]):
                return Response({
                    "status": "Error",
                    "message": "El archivo CSV debe tener exactamente las"
                    + "columnas lat y lon."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Convertir las columnas a float
            df["lat"] = df["lat"].str.replace(",", ".").astype(float)
            df["lon"] = df["lon"].str.replace(",", ".").astype(float)

            # Contar filas con NaN
            nan_rows = df[df.isnull().any(axis=1)].shape[0]

            # Contar filas con valores fuera de rango
            out_of_range_rows = df[
                (df["lat"] < -90)
                | (df["lat"] > 90)
                | (df["lon"] < -180)
                | (df["lon"] > 180)
            ].shape[0]

            # Eliminar filas con NaN
            df = df.dropna(subset=["lat", "lon"])

            # Eliminar filas con valores fuera de rango
            df = df[
                (df["lat"] >= -90)
                & (df["lat"] <= 90)
                & (df["lon"] >= -180)
                & (df["lon"] <= 180)
            ]

            file = File.objects.create(name=csv_file.name)

            coordinates = [
                Coordinate(
                    latitude=row['lat'], longitude=row['lon'], file_id=file.id
                )
                for index, row in df.iterrows()
            ]

            Coordinate.objects.bulk_create(coordinates)

            url = os.environ.get('URL_FILE_PROCESS')
            if url is not None:
                url += f"/{file.id}"
                threading.Thread(
                    target=self._async_get,
                    args=(
                        url,
                    )
                ).start()

            return Response({
                "status": "OK",
                "message": f"Se eliminaron {nan_rows} filas con valores NaN"
                + f" y {out_of_range_rows} filas con valores fuera de rango."
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class FileDetailView(APIView):
    def get(self, request):
        serializer = FileIdSerializer(data=request.query_params)
        if serializer.is_valid():
            file_id = serializer.validated_data['file_id']
            try:
                file = File.objects.annotate(
                    coordinates_processed=models.Count(
                        'coordinate', filter=models.Q(
                            coordinate__postal_code__isnull=False,
                            coordinate__file_id=file_id
                        )
                    ),
                    coordinates_total=models.Count(
                        'coordinate', filter=models.Q(
                            coordinate__file_id=file_id
                        )
                    )
                ).get(id=file_id)
                return Response(
                    {
                        "file_id": file.id,
                        "name": file.name,
                        "status": file.status,
                        "coordinates_processed": file.coordinates_processed,
                        "coordinates_total": file.coordinates_total
                    },
                    status=status.HTTP_200_OK
                )
            except File.DoesNotExist:
                return Response(
                    {"error": "File not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
