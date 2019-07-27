"""tunez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework_swagger.views import get_swagger_view
from django.views.static import serve
from .settings import BASE_DIR
from os.path import join
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

schema_view = get_swagger_view(title='ZenTunez Player API')

urlpatterns = [
    re_path(r'^react/(?P<path>.*)$', serve, {
        'document_root': join(BASE_DIR, "react"),
    }),
    path('admin/', admin.site.urls),
    path('player/', include("tunez.player.urls")),
    path('library/', include("tunez.library.urls")),
    path('swagger', schema_view)
]

# Note: Serving static files this way is not recommended for production as it
#       is not efficient.
urlpatterns += staticfiles_urlpatterns()
