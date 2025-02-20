from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

handler400 = 'performanceGC.views.error_400'
handler404 = 'performanceGC.views.error_404'
handler403 = 'performanceGC.views.error_403'
handler500 = 'performanceGC.views.error_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('performanceGC.urls')),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
