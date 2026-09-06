from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings, UsefulLink, Advertisement


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('site_name', 'footer_text', 'about_text', 'addr')


@register(UsefulLink)
class UsefulLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Advertisement)
class AdvertisementTranslationOptions(TranslationOptions):
    fields = ('title',)