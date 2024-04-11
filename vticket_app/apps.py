from django.apps import AppConfig


class VticketAccountServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vticket_app'
    app_version = 'v1'
    app_route = 'doris-account-service'
    api_prefix = f"apis/{app_route}/{app_version}/"

    def ready(self) -> None:
        super().ready()
        import vticket_app.configs.firebase_storage