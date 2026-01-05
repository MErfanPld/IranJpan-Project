from django.db import models
from django.urls import reverse
import slugify

from extenstions.utils import jalali_converter


class NewsCategory(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="عنوان دسته"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال / غیرفعال"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته خبر"
        verbose_name_plural = "دسته‌های خبری"



class News(models.Model):
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='news',
        verbose_name="دسته‌بندی"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان خبر"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ"
    )

    short_description = models.TextField(
        blank=True,
        verbose_name="خلاصه خبر"
    )

    content = models.TextField(
        verbose_name="متن کامل خبر"
    )

    image = models.ImageField(
        upload_to='news/',
        blank=True,
        null=True,
        verbose_name="تصویر شاخص"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="منتشر شده"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاریخ انتشار"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:detail', args=[self.slug])

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]  # حداکثر 50 کاراکتر
        super().save(*args, **kwargs)
        
        
    def jpublished_at(self):
        return jalali_converter(self.published_at)
    jpublished_at.short_description = 'تاریخ ایجاد'