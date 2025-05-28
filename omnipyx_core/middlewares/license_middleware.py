from django.shortcuts import redirect
from omnipyx_core.models.license import License
from django.db.utils import OperationalError


class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_path = request.path
            allowed_paths = ["/setup/", "/setup/test-db/"]

            if current_path in allowed_paths:
                return self.get_response(request)

            if not License.objects.exists():
                return redirect("/setup/")

            license_obj = License.objects.first()
            if not license_obj.is_valid():
                return redirect("/setup/?invalid_license=1")

        except OperationalError:
            # Safe fallback during migrations or no DB
            pass

        return self.get_response(request)
