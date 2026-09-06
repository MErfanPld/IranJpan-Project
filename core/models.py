from django.db import models
import time
from ckeditor_uploader.fields import RichTextUploadingField

from extenstions.utils import jalali_converter


def upload_slider_image(instance, filename):
    path = 'uploads/sliders/'
    name = f"{int(time.time())}-{filename}"
    return f"{path}{name}"


class Slider(models.Model):
    title = models.CharField("عنوان", max_length=200)
    image = models.ImageField("تصویر", upload_to=upload_slider_image)
    link = models.URLField("لینک", blank=True,null=True)
    is_active = models.BooleanField("فعال", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد")

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرها"

    def __str__(self):
        return self.title

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'

class AboutUs(models.Model):
    title = models.CharField("عنوان", max_length=255, default="درباره ما")
    content = RichTextUploadingField(verbose_name="متن")
    image = models.ImageField("تصویر", upload_to="about_us/")
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return self.title

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'

class TeamMember(models.Model):
    name = models.CharField("نام", max_length=255)
    role = models.CharField("نقش", max_length=255)
    image = models.ImageField("تصویر", upload_to="team_members/")
    facebook = models.URLField("فیسبوک", blank=True, null=True)
    twitter = models.URLField("توییتر", blank=True, null=True)
    linkedin = models.URLField("لینکدین", blank=True, null=True)
    instagram = models.URLField("اینستاگرام", blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"

    def __str__(self):
        return self.name

class JapanChamberDirectorsMember(models.Model):
    name = models.CharField("نام", max_length=255)
    role = models.CharField("نقش", max_length=255)
    image = models.ImageField("تصویر", upload_to="team_members/")
    facebook = models.URLField("فیسبوک", blank=True, null=True)
    twitter = models.URLField("توییتر", blank=True, null=True)
    linkedin = models.URLField("لینکدین", blank=True, null=True)
    instagram = models.URLField("اینستاگرام", blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "هیات مدیره اتاق ژاپن"
        verbose_name_plural = "هیات مدیره اتاق ژاپن"

    def __str__(self):
        return self.name

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'

class ContactMessage(models.Model):
    name = models.CharField("نام", max_length=255)
    email = models.EmailField("ایمیل")
    phone_number = models.CharField("تلفن", max_length=20)
    subject = models.CharField("موضوع", max_length=255)
    message = models.TextField("پیام")
    is_read = models.BooleanField("خوانده شده", default=False)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'

class Country(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="نام کشور"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال باشد"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشورها"


class GuideSection(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name="کشور"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان بخش"
    )

    description = RichTextUploadingField(
        blank=True,
        verbose_name="توضیحات"
    )

    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک مرتبط (در صورت وجود)"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال باشد"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    def __str__(self):
        return f"{self.country.name} | {self.title}"

    class Meta:
        verbose_name = "بخش راهنمای تجاری"
        verbose_name_plural = "بخش‌های راهنمای تجاری"
        ordering = ['order']

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'

class MemberAboutSection(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان "
    )

    description = RichTextUploadingField(
        blank=True,
        verbose_name="توضیحات"
    )
    
    role_description = RichTextUploadingField(
        blank=True,
        verbose_name="شرایط عضویت "
    )

    link_file = models.URLField(
        blank=True,
        null=True,
        verbose_name="لینک مرتبط (در صورت وجود)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال باشد"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "خدمات اتاق مشترک و عضویت"
        verbose_name_plural = " خدمات اتاق مشترک و عضویت ها"

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'


from django.urls import reverse

class ChamberMember(models.Model):
    full_name = models.CharField("نام و نام‌خانوادگی", max_length=255)
    company_name = models.CharField("نام شرکت", max_length=255)
    membership_code = models.CharField("کد عضویت", max_length=50, unique=True)
    position = models.CharField("سمت", max_length=255, blank=True)

    photo = models.ImageField("تصویر فرد", upload_to="chamber_members/photos/")
    company_logo = models.ImageField("لوگوی شرکت", upload_to="chamber_members/logos/", blank=True, null=True)

    bio = models.TextField("توضیحات / بیوگرافی", blank=True)

    phone_number = models.CharField("تلفن", max_length=20, blank=True)
    email = models.EmailField("ایمیل", blank=True)
    website = models.URLField("وبسایت شرکت", blank=True)
    address = models.CharField("آدرس", max_length=500, blank=True)

    catalog = models.FileField("کاتالوگ", upload_to="chamber_members/catalogs/", blank=True, null=True)

    country = models.ForeignKey(
        Country, verbose_name="کشور",
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name="chamber_members"
    )

    is_active = models.BooleanField("نمایش در سایت", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "عضو اتاق بازرگانی"
        verbose_name_plural = "اعضای اتاق بازرگانی"
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} - {self.company_name}"

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'

    def get_absolute_url(self):
        return reverse('core:chamber_member_detail', kwargs={'pk': self.pk})