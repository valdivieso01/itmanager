"""tesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from profiles.urls import profiles_patterns
from django.conf import settings
from messenger.urls import messenger_patterns
from django.views.generic import RedirectView
from django.http import HttpResponse, FileResponse
from django.conf import settings as dj_settings
import os


def favicon(request):
    path = os.path.join(dj_settings.BASE_DIR, 'core', 'static', 'core', 'img', 'favicon.ico')
    response = FileResponse(open(path, 'rb'), content_type='image/x-icon')
    response['Cache-Control'] = 'public, max-age=86400'
    return response


def favicon_png(request):
    path = os.path.join(dj_settings.BASE_DIR, 'core', 'static', 'core', 'img', 'favicon.png')
    response = FileResponse(open(path, 'rb'), content_type='image/png')
    response['Cache-Control'] = 'public, max-age=86400'
    return response


def robots_txt(request):
    content = "User-agent: *\nAllow: /\n"
    return HttpResponse(content, content_type='text/plain')


def google_site_verification(request):
    return HttpResponse(
        'google-site-verification: googlef793a724323269e7.html',
        content_type='text/html',
    )


urlpatterns = [
    path('googlef793a724323269e7.html', google_site_verification),
    path('robots.txt', robots_txt),
    re_path(r'^favicon\.ico$', favicon),
    re_path(r'^favicon\.png$', favicon_png),
    re_path(r'^apple-touch-icon\.png$', favicon_png),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    #paths de apps
    path('profiles/', include(profiles_patterns)),
    path('messenger/', include(messenger_patterns)),
    #paths de app rigistration
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls'))
]

#if settings.DEBUG:
#    from django.conf.urls.static import static
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
