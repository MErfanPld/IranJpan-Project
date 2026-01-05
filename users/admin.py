from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-created_at",)
    list_display = (
        "phone_number",
        "full_name",
        "email",
        "is_owner",
        "is_staff",
        "is_active",
    )
    search_fields = (
        "phone_number",
        "email",
        "first_name",
        "last_name",
    )

    # فرم ها
    fieldsets = (
        (_("اطلاعات کاربر"), {
            "fields": (
                "phone_number",
                "email",
                "first_name",
                "last_name",
                "bio",
                "image",
            )
        }),
        (_("دسترسی‌ها"), {
            "fields": (
                "is_active",
                "is_owner",
                "is_staff",
                "is_superuser",
            )
        }),
    )

    add_fieldsets = (
        (_("ایجاد کاربر"), {
            "classes": ("wide",),
            "fields": (
                "phone_number",
                "email",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )

    filter_horizontal = ()  # کاربر معمولی هیچ فیلد افقی نداشته باشد

    # =====================
    # محدود کردن دسترسی کاربر معمولی
    # =====================

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # سوپر یوزر همه رکوردها را می‌بیند
        return qs.filter(pk=request.user.pk)  # کاربر معمولی فقط خودش

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            # فیلدهای حساس را مخفی کن
            new_fieldsets = []
            for name, opts in fieldsets:
                fields = tuple(f for f in opts.get("fields", []) if f not in ("groups", "user_permissions", "is_superuser"))
                new_fieldsets.append((name, {"fields": fields}))
            return new_fieldsets
        return fieldsets

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.pk == request.user.pk  # فقط خودش
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None:
            return obj.pk == request.user.pk
        return False

    def has_add_permission(self, request):
        return request.user.is_superuser  # کاربر معمولی نمی‌تواند اضافه کند
