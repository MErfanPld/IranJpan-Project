from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from extenstions.utils import jalali_converter

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="عنوان دسته‌بندی"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ"
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name="عنوان تگ"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ"
    )

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="نویسنده"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='articles',
        verbose_name="دسته‌بندی"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='articles',
        verbose_name="تگ‌ها"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="عنوان مقاله"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="اسلاگ"
    )
    image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        verbose_name="تصویر مقاله"
    )
    body = RichTextUploadingField(verbose_name="محتوا")
    
    view_count = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد بازدید"
    )
    
    whats_up = models.URLField(verbose_name='لینک واتساپ', null=True,blank=True)
    instagram = models.URLField(verbose_name='لینک اینستاگرام', null=True,blank=True)

    is_published = models.BooleanField(
        default=True,
        verbose_name="منتشر شود؟"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.slug])

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'



class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="مقاله"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    text = models.TextField(
        verbose_name="متن نظر"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.user} - {self.article}"

    def jcreated_at(self):
        return jalali_converter(self.created_at)
    jcreated_at.short_description = 'تاریخ ایجاد'