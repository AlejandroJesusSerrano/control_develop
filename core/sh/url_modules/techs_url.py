from django.urls import include, path

from core.sh.views.tehcs.views import TechsDeleteView, TechsListView, TechsCreateView, TechsUpadateView

app_name = 'sh'

urlpatterns = [

  path('techs/list/', TechsListView.as_view(), name='techs_list'),
  path('techs/add/', TechsCreateView.as_view(), name='techs_add'),
  path('techs/edit/<int:pk>/', TechsUpadateView.as_view(), name='techs_edit'),
  path('techs/delete/<int:pk>/', TechsDeleteView.as_view(), name='techs_delete')

]