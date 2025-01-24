from django.urls import path

from .test_file_handler import ValidFileFormView


urlpatterns = [
    path(
        "valid-file/",
        ValidFileFormView.as_view(),
        name="valid-file",
    ),
]
