from modeltranslation.translator import register, TranslationOptions
from .models import Category, Tag, Article


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)  # slug ترجمه نشد


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'body')