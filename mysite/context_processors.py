from django.conf import settings

def site_settings(request):
    return settings.SITE_SETTINGS['site']
