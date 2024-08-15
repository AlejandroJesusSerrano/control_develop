from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from config import settings


class LoginFormView(FormView):
  form_class = AuthenticationForm
  template_name = 'login.html'
  success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return HttpResponseRedirect(self.success_url)
    return super().dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    login(self.request, form.get_user())
    next_url = self.request.POST.get('next')
    if next_url:
      return HttpResponseRedirect(next_url)
    return HttpResponseRedirect(self.success_url)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context ['title'] = 'Iniciar sesión'
    context ['next'] = self.request.GET.get('next', '')
    return context

class LogoutRedirectView(RedirectView):
  pattern_name = 'login'

  def dispatch(self, request, *args, **kwargs):
    logout(request)
    return super().dispatch(request, *args, **kwargs)
