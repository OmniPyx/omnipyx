import threading
from django.utils.deprecation import MiddlewareMixin
from django.contrib.sites.models import Site


class DynamicSiteDBMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_domain = request.get_host().split(":"[0])
        try:
            site = Site.objects.get(domain=current_domain)
            threading.local().site_db = site.name  # Assuming `name` matches DB alias
        except Site.DoesNotExist:
            threading.local().site_db = "default"
