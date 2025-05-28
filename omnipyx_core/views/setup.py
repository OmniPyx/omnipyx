from pathlib import Path

from django.shortcuts import render, redirect
from django.utils.timezone import now
from omnipyx_core.models.license import License
import hmac, hashlib, base64
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
import os


def test_db_connection(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

    engine = request.POST.get("db_engine")
    name = request.POST.get("db_name")
    user = request.POST.get("db_user")
    password = request.POST.get("db_password")
    host = request.POST.get("db_host")
    port = request.POST.get("db_port")

    alias = "test_connection"

    db_settings = {
        'ENGINE': engine,
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }

    try:
        if 'sqlite3' in engine:
            # Si es ":memory:", está bien
            if name == ":memory:":
                return JsonResponse({"success": True})

            sqlite_path = Path(f'{name}.sqlite3').resolve()

            try:
                if not sqlite_path.exists():
                    sqlite_path.touch()
                return JsonResponse({"success": True})
            except Exception as e:
                return JsonResponse({"success": False, "error": f"Cannot create SQLite DB file: {str(e)}"})

        # Para PostgreSQL, MySQL, etc.
        connections.databases[alias] = db_settings
        connections[alias].ensure_connection()
        return JsonResponse({"success": True})

    except OperationalError as e:
        return JsonResponse({"success": False, "error": str(e)})
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Unexpected error: {str(e)}"})


def setup_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        domain = request.get_host()
        issued_at = now().date()
        expires_at = issued_at.replace(year=issued_at.year + 1)
        secret_key = "SECRET_KEY_YOUR_APP_USES_TO_SIGN"
        raw_data = f"{name}|{domain}|{issued_at}|{expires_at}"
        signature = base64.b64encode(
            hmac.new(secret_key.encode(), raw_data.encode(), hashlib.sha256).digest()
        ).decode()

        License.objects.create(
            name=name,
            domain=domain,
            issued_at=issued_at,
            expires_at=expires_at,
            signature=signature,
            company_email=request.POST.get("company_email"),
            company_phone=request.POST.get("company_phone"),
            timezone=request.POST.get("timezone"),
            preferred_language=request.POST.get("preferred_language"),
            license_type=request.POST.get("license_type"),
            partner_code=request.POST.get("partner_code"),
            enable_audit=bool(request.POST.get("enable_audit")),
            accepted_terms=bool(request.POST.get("accepted_terms")),
            db_name=request.POST.get("db_name"),
            db_user=request.POST.get("db_user"),
            db_password=request.POST.get("db_password"),
            db_host=request.POST.get("db_host"),
            db_port=request.POST.get("db_port"),
            db_engine=request.POST.get("db_engine"),
        )
        return redirect("/admin/")

    return render(request, "setup.html")
