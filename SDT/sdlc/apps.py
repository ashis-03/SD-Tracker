from django.apps import AppConfig


class SdlcConfig(AppConfig):
    name = 'sdlc'

    def ready(self):
        import sdlc.signals