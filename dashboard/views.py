from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from settings.models import SiteSettings


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["membership"] = getattr(self.request.user, "membership", None)
        context['site_settings'] = SiteSettings.objects.first()
        return context
