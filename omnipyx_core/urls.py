from django.urls import path

from omnipyx_core.views.setup import setup_view, test_db_connection

urlpatterns = [
    path("setup/", setup_view, name="setup"),
    path('setup/test-db/', test_db_connection, name='test_db_connection'),
]
