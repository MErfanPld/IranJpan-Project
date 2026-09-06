from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import Category, Tag, Article, Comment
from core.translation_utils import AutoTranslateAdminMixin


@admin.register(Category)
class CategoryAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title']

    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

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


@admin.register(Tag)
class TagAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title']

    list_display = ('title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

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


class CommentInline(admin.TabularInline):  # ترجمه نمی‌شود - بدون تغییر
    model = Comment
    extra = 0
    readonly_fields = ('user', 'text', 'created_at')

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

    def has_add_permission(self, request, obj=None):
        return True


@admin.register(Article)
class ArticleAdmin(AutoTranslateAdminMixin, TabbedTranslationAdmin):
    TRANSLATABLE_FIELDS = ['title', 'body']

    list_display = (
        'title',
        'author',
        'category',
        'is_published',
        'jcreated_at',
    )
    list_filter = (
        'is_published',
        'category',
        'created_at',
    )
    search_fields = (
        'title',
        'body',
    )
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('category', 'tags')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
    inlines = [CommentInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.author == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj:
            return obj.author == request.user
        return False

    def has_add_permission(self, request):
        return True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):  # ترجمه نمی‌شود - بدون تغییر
    list_display = ('user', 'article', 'jcreated_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__phone_number')
    readonly_fields = ('created_at',)

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