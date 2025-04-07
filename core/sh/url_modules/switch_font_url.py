from django.urls import path

from core.sh.views.switch_font import views
from core.sh.views.switch_font.views import SwitchFontCreateView, SwitchFontDeleteView, SwitchFontListView, SwitchFontUpdateView

app_name = 'sh'

urlpatterns = [

  path('switch_font/list/', SwitchFontListView.as_view(), name='switch_font_list'),
  path('switch_font/add/', SwitchFontCreateView.as_view(), name='switch_font_add'),
  path('switch_font/edit/<int:pk>/', SwitchFontUpdateView.as_view(), name='switch_font_edit'),
  path('switch_font/delete/<int:pk>/', SwitchFontDeleteView.as_view(), name='switch_font_delete'),

]