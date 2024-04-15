from django.urls import path
from src.django_apps.coordinates_manager.api.views import \
    FileUploadView, FileDetailView


urlpatterns = [
    path("upload-csv", FileUploadView.as_view(), name="upload-csv"),
    path("file-detail/", FileDetailView.as_view(), name="file-detail"),
]
