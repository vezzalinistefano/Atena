from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from users.views import UserProfileView, UserProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update', UserProfileUpdateView.as_view(), name='profile-update')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
