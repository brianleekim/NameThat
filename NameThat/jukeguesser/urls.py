from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # optional, for redirecting "/" to your API
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Optional: send root "/" to your playlists endpoint
    path("", RedirectView.as_view(url="/api/playlists/", permanent=False)),

    # Admin site
    path("admin/", admin.site.urls),

    # **This** line hooks all /api/… routes into api/urls.py
    path("api/", include("api.urls")),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
