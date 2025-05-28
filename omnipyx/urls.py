from django.contrib import admin
from django.urls import path, include, re_path
from omnipyx.modules.loader import discover_omnipyx_modules

urlpatterns = [
    path('', include('omnipyx_core.urls')),
    path('admin/', admin.site.urls),
]

for module in discover_omnipyx_modules():
    module_name = module
    try:
        module_name = module.split('.')[0]
        urlpatterns.append(path(f'api/', include(f'{module_name}.urls')))
    except ModuleNotFoundError as e:
        print(f"Module {module_name} could not be loaded: {e}")

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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

# ✅ Luego de registrar módulos, agregar docs
urlpatterns += [
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
