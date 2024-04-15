from django.urls import path
from src.django_apps.postalcodes_manager.api.views import \
    FileProccessView


urlpatterns = [
    path(
        "file-proccess/<int:pk>",
        FileProccessView.as_view(),
        name="file-proccess"
    ),
]
