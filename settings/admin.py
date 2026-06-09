from django.contrib import admin
from .models import SiteSettings, UsefulLink, Advertisement


class UsefulLinkInline(admin.TabularInline):
    model = UsefulLink
    extra = 1
    min_num = 0
    verbose_name = "لینک مفید"
    verbose_name_plural = "لینک‌های مفید"

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(self.model, 'user'):
            return qs.filter(user=request.user)

        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and hasattr(obj, 'user'):
            return obj.user == request.user

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and hasattr(obj, 'user'):
            return obj.user == request.user

        return False

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'updated_at')
    inlines = [UsefulLinkInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if hasattr(self.model, 'user'):
            return qs.filter(user=request.user)

        return qs

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and hasattr(obj, 'user'):
            return obj.user == request.user

        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if obj and hasattr(obj, 'user'):
            return obj.user == request.user

        return False

    def has_add_permission(self, request, obj=None):
        # فقط یک رکورد SiteSettings مجاز باشد
        return SiteSettings.objects.count() == 0


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title',)