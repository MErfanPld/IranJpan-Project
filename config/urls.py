"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from core.views import (
    Error404View,
    Error500View,
    Error403View,
    Error400View
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # لازم برای فرم تعویض زبان
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('blogs/', include('blogs.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('news/', include('news.urls')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = Error404View.as_view()
handler500 = Error500View.as_view()
handler403 = Error403View.as_view()
handler400 = Error400View.as_view()