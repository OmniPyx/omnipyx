from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import hashlib
import hmac
import base64


class License(models.Model):
    name = models.CharField(_("Customer Name"), max_length=255)
    domain = models.CharField(_("Domain"), max_length=255, unique=True)
    issued_at = models.DateField(_("Issued At"))
    expires_at = models.DateField(_("Expires At"))
    signature = models.TextField(_("Signature"))

    company_email = models.EmailField(_("Company Email"), blank=True, null=True)
    company_phone = models.CharField(_("Company Phone"), max_length=20, blank=True, null=True)
    timezone = models.CharField(_("Timezone"), max_length=100, blank=True, null=True)
    preferred_language = models.CharField(_("Preferred Language"), max_length=10, default='en')
    logo = models.ImageField(_("Company Logo"), upload_to='logos/', blank=True, null=True)
    license_type = models.CharField(_("License Type"), max_length=50, default="full")
    partner_code = models.CharField(_("Partner Code"), max_length=50, blank=True, null=True)
    enable_audit = models.BooleanField(_("Enable Audit Log"), default=True)
    accepted_terms = models.BooleanField(_("Accepted Terms & Conditions"), default=False)

    db_name = models.CharField(_("Database Name"), max_length=100)
    db_user = models.CharField(_("Database User"), max_length=100)
    db_password = models.CharField(_("Database Password"), max_length=255)
    db_host = models.CharField(_("Database Host"), max_length=255, default='localhost')
    db_port = models.CharField(_("Database Port"), max_length=10, default='5432')
    db_engine = models.CharField(_("Database Engine"), max_length=100, default='django.db.backends.postgresql')

    def is_valid(self):
        if self.expires_at < timezone.now().date():
            return False
        return self.verify_signature()

    def verify_signature(self):
        secret_key = "SECRET_KEY_YOUR_APP_USES_TO_SIGN"  # use env variable in production
        raw_data = f"{self.name}|{self.domain}|{self.issued_at}|{self.expires_at}"
        expected_signature = base64.b64encode(
            hmac.new(secret_key.encode(), raw_data.encode(), hashlib.sha256).digest()
        ).decode()
        return hmac.compare_digest(self.signature, expected_signature)

    def __str__(self):
        return f"License for {self.domain}"
