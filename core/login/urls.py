from django.urls import path

from core.login.views import LoginFormView, LogoutRedirectView

urlpatterns = [
  path('', LoginFormView.as_view(), name='login'),
  path('logout/', LogoutRedirectView.as_view(), name='logout'),
]