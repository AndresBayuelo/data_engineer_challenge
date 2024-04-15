from django.db import models
from src.domain.postalcodes_manager.constants import \
    FileStatus, CoordinateProcessStatus


# Create your models here.
class File(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[(status.value, status.value) for status in FileStatus],
        default=FileStatus.IN_PROCESS.value,
    )

    class Meta:
        db_table = "file"


class Coordinate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    postal_code = models.CharField(max_length=10, null=True)
    process_status = models.CharField(
        max_length=50,
        choices=[
            (status.value, status.value) for status in CoordinateProcessStatus
        ],
        default=CoordinateProcessStatus.PENDING.value,
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        db_table = "coordinate"


class RequestApi(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=255)
    response = models.JSONField()

    class Meta:
        db_table = "request_api"
