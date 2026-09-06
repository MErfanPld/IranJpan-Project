from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin

from .models import (
    ChamberMember, ContactMessage, Slider, JapanChamberDirectorsMember,
    MemberAboutSection, AboutUs, TeamMember, Country, GuideSection
)
from .translation_utils import AutoTranslateAdminMixin

admin.site.site_header = "پنل مدیریت اتاق بازرگاني ايران و ژاپن"
admin.site.site_title = "داشبورد"
admin.site.index_title = "خوش آمدید"


@admin.register(Slider)
class SliderAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title']

    list_display = ("title", 'link', "is_active", "image_preview")
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    readonly_fields = ("image_preview",)
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("title", 'link', "image", "image_preview", "is_active", "created_at")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" style="object-fit: cover;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "پیش‌نمایش تصویر"

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
        return True


@admin.register(AboutUs)
class AboutUsAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title', 'content']

    list_display = ('title', 'jcreated_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'content', 'image')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

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
        return True


@admin.register(TeamMember)
class TeamMemberAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['name', 'role']

    list_display = ('name', 'role')
    list_filter = ('role',)
    search_fields = ('name', 'role')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('name', 'role', 'image')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('facebook', 'twitter', 'linkedin', 'instagram')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at',),
        }),
    )

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
        return True


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):  # ترجمه نمی‌شود - بدون تغییر
    list_display = ('name', 'email', 'phone_number', 'subject', 'is_read', 'jcreated_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone_number', 'subject', 'message', 'created_at')

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
        return True


@admin.register(JapanChamberDirectorsMember)
class JapanChamberDirectorsMemberAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['name', 'role']

    list_display = ('name', 'role', 'jcreated_at')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'role')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('name', 'role', 'image')
        }),
        ('شبکه‌های اجتماعی', {
            'fields': ('facebook', 'twitter', 'linkedin', 'instagram')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at',),
        }),
    )

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
        return True


@admin.register(Country)
class CountryAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['name']

    list_display = ('name', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name',)

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
        return True


@admin.register(GuideSection)
class GuideSectionAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title', 'description']

    list_display = ('title', 'country', 'order', 'is_active')
    list_filter = ('country', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order',)

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
        return True


@admin.register(MemberAboutSection)
class MemberAboutSectionAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title', 'description', 'role_description']

    list_display = ('title', 'is_active')
    list_filter = ['is_active']
    search_fields = ('title', 'description')

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
        return True


@admin.register(ChamberMember)
class ChamberMemberAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['full_name', 'company_name', 'position', 'bio', 'address']

    list_display = ('full_name', 'company_name', 'membership_code', 'position', 'is_active', 'jcreated_at')
    list_filter = ('is_active', 'country')
    search_fields = ('full_name', 'company_name', 'membership_code')
    list_editable = ('is_active',)