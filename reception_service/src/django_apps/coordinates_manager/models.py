from django.db import models
from src.domain.coordinates_manager.constants import FileStatus


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
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        db_table = "coordinate"
