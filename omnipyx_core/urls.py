from django.urls import path

from omnipyx_core.views.setup import setup_view

urlpatterns = [
    path("setup/", setup_view, name="setup")
]
