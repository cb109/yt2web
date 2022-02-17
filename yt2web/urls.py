from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from yt2web.core import views

urlpatterns = [
    path("playlist/<int:playlist_id>", views.playlist, name="playlist"),
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="admin/")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
