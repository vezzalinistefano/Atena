from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.views import UserProfileView

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
