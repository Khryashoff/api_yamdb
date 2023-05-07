from django.urls import path
from . import views

app_name = 'api_users'

urlpatterns = [
    path('auth/signup/', views.signup, name='signup'),
    path('auth/token/', views.token, name='token'),
]
