"""
این میدل‌ور باعث میشه سایت همیشه اول فارسی باز بشه (طبق LANGUAGE_CODE)،
حتی اگه زبان مرورگر کاربر انگلیسی یا ژاپنی باشه.

جنگو به‌صورت پیش‌فرض هدر Accept-Language مرورگر رو برای تشخیص زبان اولویت‌بندی
می‌کنه - این میدل‌ور اون هدر رو (فقط وقتی کاربر هنوز زبانی رو دستی انتخاب نکرده)
نادیده می‌گیره تا فارسی همیشه اول نمایش داده بشه.

بعد از اینکه کاربر از سوییچر زبان یه زبان رو انتخاب کنه، جنگو یه کوکی
(django_language) ذخیره می‌کنه؛ در اون حالت این میدل‌ور کاری به کار
Accept-Language نداره و انتخاب کاربر همیشه محترم شمرده میشه.
"""
from django.conf import settings


class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cookie_name = getattr(settings, "LANGUAGE_COOKIE_NAME", "django_language")
        if not request.COOKIES.get(cookie_name):
            request.META["HTTP_ACCEPT_LANGUAGE"] = ""
        return self.get_response(request)