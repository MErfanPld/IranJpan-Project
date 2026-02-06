from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from extenstions.utils import jalali_converter

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


from django.utils import timezone

class Message(models.Model):
    """مدل پیام‌ها"""
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='فرستنده'
    )
    
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        verbose_name='گیرنده'
    )
    
    message = models.TextField(verbose_name='متن پیام', blank=True)
    
    image = models.ImageField(
        upload_to='messages/%Y/%m/%d/',
        verbose_name='عکس',
        blank=True,
        null=True
    )
    
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='تاریخ ارسال'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'
    
    def __str__(self):
        return f'{self.sender} -> {self.receiver} ({self.created_at})'
    
    def get_message_preview(self):
        """پیش‌نمایش پیام"""
        if self.message:
            return self.message[:50]
        elif self.image:
            return '🖼️ عکس'
        return 'پیام خالی'
    
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'