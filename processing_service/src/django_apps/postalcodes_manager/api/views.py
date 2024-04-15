import logging
import requests
from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from src.django_apps.postalcodes_manager.models import \
    File, Coordinate, RequestApi

from src.domain.postalcodes_manager.constants import \
    CoordinateProcessStatus as ProcessStatus

logger = logging.getLogger(__name__)


# Create your views here.
class FileProccessView(APIView):
    def get(self, request, pk, format=None):
        coordinates = Coordinate.objects.filter(file_id=pk)
        if not coordinates:
            logger.error(
                'No se encontraron coordenadas para el archivo con id %s', pk
            )
            return Response(status=status.HTTP_200_OK)

        if self._validate_processed_file(pk):
            return Response(status=status.HTTP_200_OK)

        for coordinate in coordinates:
            today_min = datetime.combine(datetime.today(), datetime.min.time())
            today_max = datetime.combine(datetime.today(), datetime.max.time())
            requests_today = RequestApi.objects.filter(
                created_at__range=(today_min, today_max)
            ).count()
            if requests_today >= 20:
                logger.error(
                    'Se ha alcanzado el límite de 20 peticiones diarias.'
                )
                break

            url = "https://api.postcodes.io/outcodes"
            response = requests.get(
                url, params={
                    'lon': coordinate.longitude,
                    'lat': coordinate.latitude
                }
            )
            RequestApi.objects.create(url=url, response=response.json())

            if response.status_code == 200:
                data = response.json()
                if data and 'result' in data and data['result']:
                    outcode = data['result'][0]['outcode']
                    coordinate.postal_code = outcode
                    coordinate.process_status = ProcessStatus.PROCESSED.value
                    coordinate.save()
                else:
                    coordinate.process_status = ProcessStatus.NOT_FOUND.value
                    coordinate.save()
                    logger.error(
                        'No se encontró código postal para la coordenada'
                        + ' con id %s', coordinate.id
                    )
            else:
                logger.error(
                    'Error en la petición GET para la'
                    + ' coordenada con id %s', coordinate.id
                )

        self._validate_processed_file(pk)
        return Response(status=status.HTTP_200_OK)

    def _validate_processed_file(self, pk):
        coordinates = Coordinate.objects.filter(
            file_id=pk, process_status=ProcessStatus.PENDING.value
        )
        if not coordinates:
            logger.error(
                'Todas las coordenadas del archivo con'
                + ' id %s ya fueron procesadas', pk
            )
            file = File.objects.get(pk=pk)
            file.status = ProcessStatus.PROCESSED.value
            file.save()
            return True
        return False
