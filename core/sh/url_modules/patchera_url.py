from django.urls import include, path

from core.sh.views.patchera.views import PatcheraCreateView, PatcheraDeleteView, PatcheraListView, PatcheraUpadateView

app_name = 'sh'

urlpatterns = [

  path('patchera/list/', PatcheraListView.as_view(), name='patchera_list'),
  path('patchera/add/', PatcheraCreateView.as_view(), name='patchera_add'),
  path('patchera/edit/<int:pk>/', PatcheraUpadateView.as_view(), name='patchera_edit'),
  path('patchera/delete/<int:pk>/', PatcheraDeleteView.as_view(), name='patchera_delete'),

]