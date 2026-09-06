from modeltranslation.translator import register, TranslationOptions
from .models import (
    Slider,
    AboutUs,
    TeamMember,
    JapanChamberDirectorsMember,
    Country,
    GuideSection,
    MemberAboutSection,
    ChamberMember,
)


@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(TeamMember)
class TeamMemberTranslationOptions(TranslationOptions):
    fields = ('name', 'role')


@register(JapanChamberDirectorsMember)
class JapanChamberDirectorsMemberTranslationOptions(TranslationOptions):
    fields = ('name', 'role')


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)  # slug عمداً ترجمه نشد


@register(GuideSection)
class GuideSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MemberAboutSection)
class MemberAboutSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'role_description')


@register(ChamberMember)
class ChamberMemberTranslationOptions(TranslationOptions):
    fields = ('full_name', 'company_name', 'position', 'bio', 'address')