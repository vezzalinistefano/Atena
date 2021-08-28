from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from core.views import Maintenance, NotFound, Homepage, AccessForbidden

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('admin/', admin.site.urls),
    path('maintenance', Maintenance.as_view(), name='maintenance'),
    path('404-not-found', NotFound.as_view(), name='404-not-found'),
    path('forbidden', AccessForbidden.as_view(), name='access-forbidden'),
    path('shop/', include('shop.urls')),
    path('users/', include('users.urls')),
    path('authentication/', include('authentication.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
