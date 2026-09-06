from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from .models import SiteSettings, UsefulLink, Advertisement
from core.translation_utils import AutoTranslateAdminMixin


class UsefulLinkInline(TranslationTabularInline):
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
class SiteSettingsAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['site_name', 'footer_text', 'about_text', 'addr']

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
        return SiteSettings.objects.count() == 0


@admin.register(Advertisement)
class AdvertisementAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title']

    list_display = ('title',)