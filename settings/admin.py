from django.contrib import admin
from .models import SiteSettings, UsefulLink,Advertisement

class UsefulLinkInline(admin.TabularInline):
    model = UsefulLink
    extra = 1  
    min_num = 0
    verbose_name = "لینک مفید"
    verbose_name_plural = "لینک‌های مفید"

    # -------------------------
    # محدود کردن دسترسی کاربران
    # -------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.user == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.user == request.user
        return False

    def has_add_permission(self, request):
        return True  # همه می‌توانند کامنت اضافه کنند

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'updated_at')
    inlines = [UsefulLinkInline]

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists() or super().has_add_permission(request)

    # -------------------------
    # محدود کردن دسترسی کاربران
    # -------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.user == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.user == request.user
        return False

    def has_add_permission(self, request):
        return True  # همه می‌توانند کامنت اضافه کنند

admin.site.register(Advertisement)
