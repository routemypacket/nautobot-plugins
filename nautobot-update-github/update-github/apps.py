from django.apps import AppConfig

class UpdateGithubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'update_github'
    verbose_name = "Update GitHub"

    def ready(self):
        import update_github.jobs  # noqa: F401