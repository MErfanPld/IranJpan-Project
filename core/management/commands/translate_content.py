"""
Management Command: ترجمه‌ی خودکار محتوای دیتابیس (فارسی -> انگلیسی/ژاپنی)
با استفاده از Google Translate رایگان (deep-translator)

نحوه‌ی اجرا:
    python manage.py translate_content

⚠️ این ترجمه‌ی ماشینیه، حتماً بعداً از پنل ادمین بازبینی کن.
⚠️ فقط رکوردهایی که فیلد _en یا _ja خالی دارن رو پر می‌کنه.
"""
import time
from django.core.management.base import BaseCommand
from deep_translator import GoogleTranslator


def translate_text(text, target_lang, max_retries=3):
    if not text or not str(text).strip():
        return ""
    for attempt in range(max_retries):
        try:
            result = GoogleTranslator(source='fa', target=target_lang).translate(str(text))
            time.sleep(0.5)
            return result or ""
        except Exception as e:
            print(f"  خطا در ترجمه (تلاش {attempt+1}/{max_retries}): {e}")
            time.sleep(2)
    return ""


def translate_model_fields(model_class, fields, target_langs=('en', 'ja')):
    queryset = model_class.objects.all()
    total = queryset.count()
    print(f"\n=== {model_class.__name__} ({total} رکورد) ===")

    for idx, obj in enumerate(queryset, 1):
        changed = False
        for field in fields:
            fa_value = getattr(obj, f"{field}_fa", None) or getattr(obj, field, None)
            if not fa_value:
                continue

            for lang in target_langs:
                target_field = f"{field}_{lang}"
                if not hasattr(obj, target_field):
                    continue
                current_value = getattr(obj, target_field, None)
                if current_value:
                    continue

                translated = translate_text(fa_value, lang)
                setattr(obj, target_field, translated)
                changed = True

        if changed:
            obj.save()
            print(f"  [{idx}/{total}] ترجمه شد: {obj}")
        else:
            print(f"  [{idx}/{total}] رد شد: {obj}")


class Command(BaseCommand):
    help = "ترجمه‌ی خودکار محتوای دیتابیس با گوگل ترنسلیت رایگان"

    def handle(self, *args, **options):
        from core.models import (
            ChamberMember, TeamMember, JapanChamberDirectorsMember,
            Country, GuideSection, MemberAboutSection, AboutUs, Slider,
        )
        from blogs.models import Category, Tag, Article
        from news.models import NewsCategory, News

        translate_model_fields(ChamberMember, ['full_name', 'company_name', 'position', 'bio', 'address'])
        translate_model_fields(TeamMember, ['name', 'role'])
        translate_model_fields(JapanChamberDirectorsMember, ['name', 'role'])
        translate_model_fields(Country, ['name'])
        translate_model_fields(GuideSection, ['title', 'description'])
        translate_model_fields(MemberAboutSection, ['title', 'description', 'role_description'])
        translate_model_fields(AboutUs, ['title', 'content'])
        translate_model_fields(Slider, ['title'])
        translate_model_fields(Category, ['title'])
        translate_model_fields(Tag, ['title'])
        translate_model_fields(Article, ['title', 'body'])
        translate_model_fields(NewsCategory, ['title'])
        translate_model_fields(News, ['title', 'short_description', 'content'])

        self.stdout.write(self.style.SUCCESS("\n✅ ترجمه‌ی خودکار تمام شد. حتماً از پنل ادمین بازبینی کن."))