from django.contrib import admin
from .models import Membership
from django.utils.translation import gettext_lazy as _

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "start_date", "end_date", "is_active", "days_left_display")
    search_fields = ("user__phone_number", "user__email")
    autocomplete_fields = ("user",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # superuser همه رکوردها را می‌بیند
        if request.user.is_superuser:
            return qs
        # staff معمولی فقط رکورد خودش
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        # superuser همه رکوردها را تغییر می‌دهد
        if request.user.is_superuser:
            return True
        # اگر obj مشخص باشد، فقط اگر مالک obj باشد اجازه تغییر دارد
        if obj is not None:
            return obj.user == request.user
        # اجازه دسترسی به لیست برای staff
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.user == request.user
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        # کاربر معمولی فقط می‌تواند یک رکورد خودش داشته باشد
        return not Membership.objects.filter(user=request.user).exists()

    # نمایش روز باقی مانده
    def days_left_display(self, obj):
        return obj.days_left()
    days_left_display.short_description = _("روز باقی‌مانده")
