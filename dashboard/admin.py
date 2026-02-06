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



from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """مدیریت پیام‌ها در پنل ادمین"""
    
    # فیلدهای نمایش داده شده در لیست
    list_display = [
        'id',
        'sender_link',
        'receiver_link',
        'message_preview',
        'image_thumbnail',
        'is_read_badge',
        'jcreated_at',
    ]
    
    # فیلترها
    list_filter = [
        'is_read',
        'created_at',
        ('sender', admin.RelatedOnlyFieldListFilter),
        ('receiver', admin.RelatedOnlyFieldListFilter),
    ]
    
    # جستجو - بدون فیلد username
    search_fields = [
        'sender__first_name',
        'sender__last_name',
        'sender__email',
        'receiver__first_name',
        'receiver__last_name',
        'receiver__email',
        'message',
    ]
    
    # تاریخ‌ها
    date_hierarchy = 'created_at'
    
    # فیلدهای فقط خواندنی
    readonly_fields = [
        'created_at',
        'updated_at_display',
        'image_preview',
    ]
    
    # گروه‌بندی فیلدها در فرم
    fieldsets = (
        ('اطلاعات ارسال و دریافت', {
            'fields': ('sender', 'receiver', 'is_read')
        }),
        ('محتوای پیام', {
            'fields': ('message', 'image', 'image_preview')
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at_display')
        }),
    )
    
    # تعداد آیتم‌ها در هر صفحه
    list_per_page = 25
    
    # مرتب‌سازی پیش‌فرض
    ordering = ['-created_at']
    
    # ============================================
    # متدهای کاستومایز شده برای نمایش بهتر
    # ============================================
    
    def sender_link(self, obj):
        """لینک به پروفایل فرستنده"""
        url = f"/admin/{obj.sender._meta.app_label}/{obj.sender._meta.model_name}/{obj.sender.id}/change/"
        
        # دریافت نام نمایشی کاربر
        display_name = obj.sender.get_full_name() or str(obj.sender)
        
        # دریافت فیلد اصلی کاربر (ایمیل یا هر فیلد دیگر)
        main_field = getattr(obj.sender, 'email', getattr(obj.sender, 'phone', str(obj.sender)))
        
        return format_html(
            '<a href="{}" target="_blank" style="color: #17a2b8; text-decoration: underline;">{} ({})</a>',
            url,
            display_name,
            main_field
        )
    sender_link.short_description = _('فرستنده')
    sender_link.admin_order_field = 'sender'
    
    def receiver_link(self, obj):
        """لینک به پروفایل گیرنده"""
        url = f"/admin/{obj.receiver._meta.app_label}/{obj.receiver._meta.model_name}/{obj.receiver.id}/change/"
        
        # دریافت نام نمایشی کاربر
        display_name = obj.receiver.get_full_name() or str(obj.receiver)
        
        # دریافت فیلد اصلی کاربر
        main_field = getattr(obj.receiver, 'email', getattr(obj.receiver, 'phone', str(obj.receiver)))
        
        return format_html(
            '<a href="{}" target="_blank" style="color: #28a745; text-decoration: underline;">{} ({})</a>',
            url,
            display_name,
            main_field
        )
    receiver_link.short_description = _('گیرنده')
    receiver_link.admin_order_field = 'receiver'
    
    def message_preview(self, obj):
        """پیش‌نمایش متن پیام"""
        if obj.message:
            return format_html(
                '<span title="{}">{}</span>',
                obj.message,
                (obj.message[:50] + '...') if len(obj.message) > 50 else obj.message
            )
        return format_html('<span class="text-muted">— بدون متن —</span>')
    message_preview.short_description = _('پیام')
    message_preview.admin_order_field = 'message'
    
    def image_thumbnail(self, obj):
        """تصویر بندانگشتی عکس"""
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="40" height="40" style="object-fit: cover; border-radius: 4px;" '
                'title="کلیک برای بزرگنمایی" /></a>',
                obj.image.url,
                obj.image.url
            )
        return format_html('<span class="text-muted">—</span>')
    image_thumbnail.short_description = _('عکس')
    
    def image_preview(self, obj):
        """پیش‌نمایش بزرگ عکس در فرم ویرایش"""
        if obj.image:
            return format_html(
                '<div style="max-width: 300px; margin: 10px 0;">'
                '<img src="{}" style="width: 100%; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />'
                '</div>',
                obj.image.url
            )
        return format_html('<span class="text-muted">بدون تصویر</span>')
    image_preview.short_description = _('پیش‌نمایش تصویر')
    
    def is_read_badge(self, obj):
        """نشانگر وضعیت خوانده شدن پیام"""
        if obj.is_read:
            return format_html(
                '<span class="badge bg-success" style="padding: 5px 10px; border-radius: 4px;">خوانده شده</span>'
            )
        return format_html(
            '<span class="badge bg-warning text-dark" style="padding: 5px 10px; border-radius: 4px;">جدید</span>'
        )
    is_read_badge.short_description = _('وضعیت')
    is_read_badge.admin_order_field = 'is_read'
    
    def updated_at_display(self, obj):
        """نمایش زمان آخرین بروزرسانی"""
        if hasattr(obj, 'updated_at'):
            return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        return format_html('<span class="text-muted">—</span>')
    updated_at_display.short_description = _('آخرین بروزرسانی')
    
    
    # ============================================
    # اکشن‌ها
    # ============================================
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    @admin.action(description=_('علامت‌گذاری به عنوان خوانده شده'))
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} پیام به عنوان خوانده شده علامت‌گذاری شدند.')
    
    @admin.action(description=_('علامت‌گذاری به عنوان خوانده نشده'))
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} پیام به عنوان خوانده نشده علامت‌گذاری شدند.')
    
    # ============================================
    # بهینه‌سازی کوئری‌ست
    # ============================================
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('sender', 'receiver')