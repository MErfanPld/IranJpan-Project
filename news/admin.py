from django.contrib import admin
from .models import News, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active',)
    search_fields = ('title',)

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

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_published',
        'jpublished_at'
    )
    list_filter = (
        'is_published',
        'category'
    )
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'


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