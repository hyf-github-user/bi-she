from django.apps import AppConfig


class MonitorConfig(AppConfig):
    name = 'drf_vue_element_admin.myapps.monitor'

    def ready(self):
        import drf_vue_element_admin.myapps.monitor.signals
        import drf_vue_element_admin.myapps.monitor.notification
