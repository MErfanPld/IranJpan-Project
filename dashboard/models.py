from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Membership(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="membership",
        verbose_name=_("کاربر"),
    )

    start_date = models.DateField(_("تاریخ شروع عضویت"))
    end_date = models.DateField(_("تاریخ پایان عضویت"))

    is_active = models.BooleanField(_("فعال است؟"), default=True)

    created_at = models.DateTimeField(_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاریخ ویرایش"), auto_now=True)

    class Meta:
        verbose_name = "عضویت"
        verbose_name_plural = "عضویت‌ها"

    def __str__(self):
        return f"عضویت {self.user}"

    # --------------------
    # Business Logic
    # --------------------
    def days_left(self):
        today = timezone.now().date()
        return (self.end_date - today).days

    def is_valid(self):
        today = timezone.now().date()
        return self.is_active and self.end_date >= today
