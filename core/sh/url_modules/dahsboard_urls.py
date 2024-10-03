from django.urls import path

from core.sh.views.dashboard.views import DashboardView

app_name = 'sh'

urlpatterns = [

  path('dashboard/', DashboardView.as_view(), name='dashboard')

]