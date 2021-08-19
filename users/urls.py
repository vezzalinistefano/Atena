from django.urls import path
from users.views import UserCreate, UserLogin, UserLogout


app_name = 'users'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
]