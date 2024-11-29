from django.urls import path 

from core.sh.views.movements.views import  MovementsListView, MovementsCreateView, MovementsUpdateView, MovementsDeleteView

app_name = 'sh'

urlpatterns = [

  path('movements/list/', MovementsListView.as_view(), name='movements_list'),
  path('movements/add/', MovementsCreateView.as_view(), name='movements_add' ),
  path('movements/edit/<int:pk>/', MovementsUpdateView.as_view(), name='movements_edit' ),
  path('movements/delete/<int:pk>/', MovementsDeleteView.as_view(), name='movements_delete' )

]