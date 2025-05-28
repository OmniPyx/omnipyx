from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import hashlib
import hmac
import base64
import os


class License(models.Model):
    name = models.CharField(
        verbose_name=_("Customer Name"),
        max_length=255,
        help_text=_("The full name or business name of the licensee.")
    )
    domain = models.CharField(
        verbose_name=_("Domain"),
        max_length=255,
        unique=True,
        help_text=_("The domain this license is valid for.")
    )
    issued_at = models.DateField(
        verbose_name=_("Issued At"),
        help_text=_("Date the license was issued.")
    )
    expires_at = models.DateField(
        verbose_name=_("Expires At"),
        help_text=_("Date the license expires.")
    )
    signature = models.TextField(
        verbose_name=_("Signature"),
        help_text=_("Secure signature to validate authenticity.")
    )

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")
        ordering = ["-issued_at"]

    def __str__(self):
        return f"🔐 License for {self.domain}"

    def is_valid(self):
        """Check if the license is still valid."""
        if self.expires_at < timezone.now().date():
            return False
        return self.verify_signature()

    def verify_signature(self):
        """Verify HMAC-SHA256 license signature."""
        secret_key = os.getenv("OMNIPYX_SECRET_KEY", "SECRET_KEY_YOUR_APP_USES_TO_SIGN")
        raw_data = f"{self.name}|{self.domain}|{self.issued_at}|{self.expires_at}"
        expected_signature = base64.b64encode(
            hmac.new(secret_key.encode(), raw_data.encode(), hashlib.sha256).digest()
        ).decode()
        return hmac.compare_digest(self.signature, expected_signature)
