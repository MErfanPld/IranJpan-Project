from django.contrib import admin
from django.utils.html import format_html

from .models import ContactMessage, Slider,JapanChamberDirectorsMember,MemberAboutSection


admin.site.site_header = "پنل مدیریت اتاق بازرگاني ايران و ژاپن"
admin.site.site_title = "داشبورد"
admin.site.index_title = "خوش آمدید"


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "image_preview")
    list_filter = ("is_active", "created_at")
    search_fields = ("title",)
    readonly_fields = ("image_preview",)
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("title", "image", "image_preview", "is_active")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" style="object-fit: cover;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "پیش‌نمایش تصویر"
    

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
   
from .models import AboutUs, TeamMember

# -----------------------------
# Admin حرفه‌ای برای AboutUs
# -----------------------------
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
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

# -----------------------------
# Admin حرفه‌ای برای TeamMember
# -----------------------------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    list_filter = ('role',)
    search_fields = ('name', 'role')
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

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject', 'is_read', 'jcreated_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone_number', 'subject', 'message', 'created_at')
    
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
    
@admin.register(JapanChamberDirectorsMember)
class JapanChamberDirectorsMemberAdmin(admin.ModelAdmin):
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

from .models import Country, GuideSection


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)
    search_fields = ('name',)

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

@admin.register(GuideSection)
class GuideSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'order', 'is_active')
    list_filter = ('country', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order',)

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

@admin.register(MemberAboutSection)
class MemberAboutSectionAdmin(admin.ModelAdmin):
    list_display = ('title','is_active')
    list_filter = ['is_active']
    search_fields = ('title', 'description')
    
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