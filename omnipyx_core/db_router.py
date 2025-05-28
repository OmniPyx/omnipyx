class SiteDatabaseRouter:
    def db_for_read(self, model, **hints):
        return self._get_db_for_request()

    def db_for_write(self, model, **hints):
        return self._get_db_for_request()

    def _get_db_for_request(self):
        import threading
        return getattr(threading.local(), "site_db", "default")

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
