from modeltranslation.translator import register, TranslationOptions
from .models import NewsCategory, News


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'content')