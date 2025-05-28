from django.shortcuts import redirect
from omnipyx_core.models.license import License


class LicenseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.db.utils import OperationalError

        if request.path.startswith("/setup/"):
            return self.get_response(request)

        try:
            if not License.objects.exists():
                return redirect("/setup/")
            license_obj = License.objects.first()
            if not license_obj.is_valid():
                return redirect("/setup/?invalid_license=1")
        except OperationalError:
            pass  # During initial migrations

        return self.get_response(request)
