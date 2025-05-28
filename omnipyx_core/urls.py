"""
URL configuration for omnipyx_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from omnipyx_core.modules.loader import discover_omnipyx_modules

schema_view = get_schema_view(
    openapi.Info(
        title="Omnipyx API",
        default_version='v1',
        description="Documentación dinámica para todos los módulos instalados.",
        terms_of_service="https://zentryx.com/terms/",
        contact=openapi.Contact(email="contact@zentryx.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

for module_name in discover_omnipyx_modules():
    try:
        urlpatterns.append(path(f'api/{module_name}/', include(f'{module_name}.urls')))
    except ModuleNotFoundError:
        continue
