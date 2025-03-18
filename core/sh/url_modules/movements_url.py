from django.urls import path

from core.sh.views.movements.views import  MovementsDetailsView, MovementsListView, MovementsCreateView, MovementsUpdateView, MovementsDeleteView

app_name = 'sh'

urlpatterns = [

  path('move/list/', MovementsListView.as_view(), name='move_list'),
  path('move/add/', MovementsCreateView.as_view(), name='move_add' ),
  path('move/edit/<int:pk>/', MovementsUpdateView.as_view(), name='move_edit' ),
  path('move/delete/<int:pk>/', MovementsDeleteView.as_view(), name='move_delete' ),
  path('move/details/<int:pk>/', MovementsDetailsView.as_view(), name='move_details' )

]