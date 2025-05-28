import base64
import hashlib
import hmac

from django.contrib.sites.models import Site
from django.shortcuts import redirect, render
from django.utils.timezone import now


def setup_view(request):
    from omnipyx_core.models.license import License

    if License.objects.exists():
        return redirect("/admin/")  # prevent re-setup if already exists

    if request.method == "POST":
        name = request.POST.get("name")
        domain = request.get_host().split(":")[0]
        issued_at = now().date()
        expires_at = issued_at.replace(year=issued_at.year + 1)

        # Create signature
        secret_key = "SECRET_KEY_YOUR_APP_USES_TO_SIGN"
        raw_data = f"{name}|{domain}|{issued_at}|{expires_at}"
        signature = base64.b64encode(
            hmac.new(secret_key.encode(), raw_data.encode(), hashlib.sha256).digest()
        ).decode()

        # Create Site if not exist
        site, _ = Site.objects.get_or_create(domain=domain, defaults={"name": domain})

        # Create License
        License.objects.create(
            name=name,
            domain=domain,
            issued_at=issued_at,
            expires_at=expires_at,
            signature=signature
        )
        return redirect("/admin/")

    return render(request, "setup.html")
