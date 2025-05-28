from django.contrib import admin
from omnipyx_core.models.license import License
from django.utils.html import format_html
from django.utils.timezone import now


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "issued_at", "expires_at", "valid_status", "short_signature")
    search_fields = ("name", "domain")
    readonly_fields = ("signature", "valid_status")

    def valid_status(self, obj):
        color = "green" if obj.is_valid() else "red"
        label = "✔️ Valid" if obj.is_valid() else "❌ Expired"
        return format_html('<strong style="color:{};">{}</strong>', color, label)

    valid_status.short_description = "Status"

    def short_signature(self, obj):
        return obj.signature[:15] + "..."

    short_signature.short_description = "Signature"
