# from django.urls import include, path
# # from django.views.generic import TemplateView
# from rest_framework.routers import DefaultRouter

# from users.views import (UserViewSet, get_token, register_user)


# router_v1 = DefaultRouter()
# router_v1.register(r'users', UserViewSet, basename='users')

# urlpatterns_auth = [
#     path('signup/', register_user, name='register_user'),
#     path('token/', get_token, name='token'),
# ]

# from django.urls import path
# from . import views

# app_name = 'api_users'

# urlpatterns = [
#     path('auth/signup/', views.signup, name='signup'),
#     path('auth/token/', views.token, name='token'),
# ]
