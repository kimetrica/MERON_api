"""urls.py that just renders a template to enable test usage of the API."""

from django.views.generic.base import TemplateView
from django.urls import path


app_name = "frontend"

urlpatterns = [
    path("", TemplateView.as_view(template_name="frontend.html"), name="frontend")
]
