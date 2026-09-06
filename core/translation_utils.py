"""
ابزار مشترک ترجمه‌ی خودکار - برای استفاده در اکشن‌های پنل ادمین
"""
import time
from deep_translator import GoogleTranslator


def translate_text(text, target_lang, max_retries=3):
    if not text or not str(text).strip():
        return ""
    for attempt in range(max_retries):
        try:
            result = GoogleTranslator(source='fa', target=target_lang).translate(str(text))
            time.sleep(0.3)
            return result or ""
        except Exception:
            time.sleep(1.5)
    return ""


class AutoTranslateAdminMixin:
    """
    این Mixin رو به هر ادمینی که TabbedTranslationAdmin استفاده می‌کنه اضافه کن.
    باید یه اتریبیوت TRANSLATABLE_FIELDS توی کلاس ادمین تعریف کنی:
        TRANSLATABLE_FIELDS = ['title', 'body']
    """
    TRANSLATABLE_FIELDS = []
    actions = ['auto_translate_selected']

    def auto_translate_selected(self, request, queryset):
        target_langs = ('en', 'ja')
        updated_count = 0

        for obj in queryset:
            changed = False
            for field in self.TRANSLATABLE_FIELDS:
                fa_value = getattr(obj, f"{field}_fa", None)
                if not fa_value:
                    continue

                for lang in target_langs:
                    target_field = f"{field}_{lang}"
                    if not hasattr(obj, target_field):
                        continue
                    current_value = getattr(obj, target_field, None)
                    if current_value:
                        continue  # چیزی که از قبل پر بوده رو خراب نکن

                    translated = translate_text(fa_value, lang)
                    setattr(obj, target_field, translated)
                    changed = True

            if changed:
                obj.save()
                updated_count += 1

        if updated_count:
            self.message_user(request, f"{updated_count} رکورد با ترجمه‌ی خودکار پر شد. لطفاً بازبینی کن.")
        else:
            self.message_user(request, "همه‌ی رکوردهای انتخابی از قبل ترجمه داشتن یا محتوای فارسی خالی بود.")

    auto_translate_selected.short_description = "ترجمه‌ی خودکار (پیش‌نویس EN/JA)"