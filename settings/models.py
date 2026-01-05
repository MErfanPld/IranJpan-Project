from django.db import models

from extenstions.utils import jalali_converter

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, verbose_name="نام سایت")
    logo = models.ImageField(upload_to='site_logo/', verbose_name="لوگو", blank=True, null=True)
    footer_text = models.TextField(verbose_name="متن فوتر", blank=True)
    phone = models.CharField(max_length=200,verbose_name='شماره تماس',blank=True)
    email = models.EmailField(max_length=200,verbose_name='ایمیل',blank=True)
    addr = models.TextField(verbose_name='آدرس', blank=True)
    about_text = models.TextField(verbose_name="متن درباره اتاق صفحه اول", blank=True)
    about_img = models.ImageField(upload_to='site_about/', verbose_name="تصویر درباره اتاق", blank=True, null=True)

    # شبکه‌های اجتماعی
    whats_app = models.URLField(verbose_name="لینک واتس اپ", blank=True)
    twitter = models.URLField(verbose_name="لینک توییتر", blank=True)
    instagram = models.URLField(verbose_name="لینک اینستاگرام", blank=True)
    linkedin = models.URLField(verbose_name="لینک لینکدین", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return "تنظیمات وب‌سایت"

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'
    

class UsefulLink(models.Model):
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='useful_links')
    title = models.CharField(max_length=200, verbose_name="عنوان لینک")
    url = models.URLField(verbose_name="آدرس لینک")

    class Meta:
        verbose_name = "لینک مفید"
        verbose_name_plural = "لینک‌های مفید"

    def __str__(self):
        return self.title
    
    
class Advertisement(models.Model):
    title = models.CharField("عنوان", max_length=200)
    image = models.ImageField("تصویر", upload_to='site_logo/')
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "تبلیغ"
        verbose_name_plural = "تبلیغات"

    def __str__(self):
        return self.title
    
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'