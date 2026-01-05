from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)

        if not form.cleaned_data.get("remember_me"):
            self.request.session.set_expiry(0)

        return super().form_valid(form)


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LogoutView(FormView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("accounts:login")
