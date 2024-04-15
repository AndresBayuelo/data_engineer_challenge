from rest_framework import serializers


class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Debe ser un archivo CSV")
        return value


class FileIdSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
