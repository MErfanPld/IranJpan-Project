"""
Django Project & Admin Panel Full Test Script
=============================================
دستور اجرا:
    python test_django_project.py

یا اگه settings خاص داری:
    python test_django_project.py --settings=myproject.settings.production
"""

import os
import sys
import argparse
import importlib
import traceback
from io import StringIO

# ── رنگ‌ها برای ترمینال ──────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

passed = []
failed = []
warnings = []


def ok(msg):
    passed.append(msg)
    print(f"  {GREEN}✔ {msg}{RESET}")


def fail(msg, detail=""):
    failed.append(msg)
    print(f"  {RED}✘ {msg}{RESET}")
    if detail:
        print(f"    {RED}↳ {detail}{RESET}")


def warn(msg):
    warnings.append(msg)
    print(f"  {YELLOW}⚠ {msg}{RESET}")


def section(title):
    print(f"\n{CYAN}{BOLD}{'─'*55}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{BOLD}{'─'*55}{RESET}")


# ── ۱. راه‌اندازی Django ──────────────────────────────────────────────────────
def setup_django(settings_module=None):
    section("۱. راه‌اندازی Django")

    # پیدا کردن خودکار settings
    if not settings_module:
        for candidate in ["config.settings", "settings", "core.settings",
                          "myproject.settings", "app.settings"]:
            try:
                importlib.import_module(candidate)
                settings_module = candidate
                break
            except ModuleNotFoundError:
                continue

    if not settings_module:
        fail("فایل settings پیدا نشد", "با --settings مشخص کن")
        sys.exit(1)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    try:
        import django
        django.setup()
        ok(f"Django {django.__version__} راه‌اندازی شد ({settings_module})")
        return True
    except Exception as e:
        fail("django.setup() شکست خورد", str(e))
        sys.exit(1)


# ── ۲. تست دیتابیس ───────────────────────────────────────────────────────────
def test_database():
    section("۲. اتصال به دیتابیس")
    from django.db import connections, OperationalError

    for alias in connections:
        try:
            conn = connections[alias]
            conn.ensure_connection()
            ok(f"دیتابیس '{alias}' متصل است")
        except OperationalError as e:
            fail(f"دیتابیس '{alias}' متصل نشد", str(e))


# ── ۳. تست Migration ─────────────────────────────────────────────────────────
def test_migrations():
    section("۳. وضعیت Migration‌ها")
    from django.db.migrations.executor import MigrationExecutor
    from django.db import connection

    try:
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        if plan:
            for migration, _ in plan:
                warn(f"Migration اجرا نشده: {migration.app_label}.{migration.name}")
        else:
            ok("همه migration‌ها اعمال شده‌اند")
    except Exception as e:
        fail("بررسی migration شکست خورد", str(e))


# ── ۴. تست پنل ادمین ─────────────────────────────────────────────────────────
def test_admin_panel():
    section("۴. پنل ادمین Django")

    from django.contrib import admin
    from django.contrib.auth import get_user_model
    from django.test import RequestFactory, Client
    from django.contrib.admin.sites import AdminSite

    User = get_user_model()

    # --- ساختن superuser موقت (سازگار با Custom User Model) ---
    password        = "Test@12345!"
    username_field  = User.USERNAME_FIELD          # phone_number / email / username
    unique_val      = {
        "email":        "test_tmp_admin@example.com",
        "phone_number": "09000000000",
    }.get(username_field, "_test_superuser_tmp_")

    extra = {}
    # اگه email فیلد جداگانه‌ای داره (و USERNAME_FIELD نیست) اضافه کن
    if username_field != "email" and "email" in [f.name for f in User._meta.get_fields()]:
        try:
            User._meta.get_field("email")
            extra["email"] = "test_tmp_admin@example.com"
        except Exception:
            pass

    create_kwargs = {username_field: unique_val, "password": password, **extra}

    try:
        user = User.objects.filter(**{username_field: unique_val}).first()
        if not user:
            user = User.objects.create_superuser(**create_kwargs)
        ok(f"Superuser موقت ساخته/یافته شد ({username_field}={unique_val!r})")
    except Exception as e:
        fail("ساخت superuser شکست خورد", str(e))
        return

    client = Client()

    # --- لاگین ---
    logged_in = client.login(**{username_field: unique_val, "password": password})
    if logged_in:
        ok("لاگین به پنل ادمین موفق بود")
    else:
        fail("لاگین به پنل ادمین شکست خورد")
        _cleanup_user(user)
        return

    # --- صفحه اصلی ادمین ---
    try:
        resp = client.get("/admin/", follow=True)
        if resp.status_code == 200:
            ok("صفحه اصلی /admin/ بارگذاری شد (200)")
        else:
            fail(f"صفحه /admin/ کد {resp.status_code} برگرداند")
    except Exception as e:
        fail("/admin/ بارگذاری نشد", str(e))

    # --- تست هر مدل ثبت‌شده در ادمین ---
    site = admin.site
    registry = site._registry

    if not registry:
        warn("هیچ مدلی در ادمین ثبت نشده است")
    else:
        ok(f"{len(registry)} مدل در ادمین ثبت شده است")

    for model, model_admin in registry.items():
        app   = model._meta.app_label
        model_name = model._meta.model_name
        base_url = f"/admin/{app}/{model_name}/"

        # ۴-۱. لیست
        try:
            resp = client.get(base_url, follow=True)
            if resp.status_code == 200:
                ok(f"[{app}.{model_name}] صفحه list بارگذاری شد")
            else:
                fail(f"[{app}.{model_name}] list → کد {resp.status_code}")
        except Exception as e:
            fail(f"[{app}.{model_name}] list خطا", str(e))

        # ۴-۲. فرم add
        try:
            resp = client.get(f"{base_url}add/", follow=True)
            if resp.status_code == 200:
                ok(f"[{app}.{model_name}] صفحه add بارگذاری شد")
            elif resp.status_code == 403:
                warn(f"[{app}.{model_name}] add → 403 (دسترسی محدود)")
            else:
                fail(f"[{app}.{model_name}] add → کد {resp.status_code}")
        except Exception as e:
            fail(f"[{app}.{model_name}] add خطا", str(e))

        # ۴-۳. اگر رکورد وجود دارد → صفحه change
        try:
            obj = model.objects.first()
            if obj:
                resp = client.get(f"{base_url}{obj.pk}/change/", follow=True)
                if resp.status_code == 200:
                    ok(f"[{app}.{model_name}] صفحه change (pk={obj.pk}) بارگذاری شد")
                elif resp.status_code == 403:
                    warn(f"[{app}.{model_name}] change → 403")
                else:
                    fail(f"[{app}.{model_name}] change → کد {resp.status_code}")
            else:
                warn(f"[{app}.{model_name}] رکوردی برای تست change وجود ندارد")
        except Exception as e:
            fail(f"[{app}.{model_name}] change خطا", str(e))

    # --- جست‌وجو در ادمین ---
    for model, model_admin in registry.items():
        if model_admin.search_fields:
            app = model._meta.app_label
            model_name = model._meta.model_name
            try:
                resp = client.get(
                    f"/admin/{app}/{model_name}/?q=test", follow=True
                )
                if resp.status_code == 200:
                    ok(f"[{app}.{model_name}] جست‌وجوی ادمین کار می‌کند")
                else:
                    fail(f"[{app}.{model_name}] جست‌وجو → کد {resp.status_code}")
            except Exception as e:
                fail(f"[{app}.{model_name}] جست‌وجو خطا", str(e))

    _cleanup_user(user)


def _cleanup_user(user):
    try:
        user.delete()
        ok("Superuser موقت حذف شد")
    except Exception as e:
        warn(f"حذف superuser موقت ناموفق: {e}")


# ── ۵. تست URL‌ها ─────────────────────────────────────────────────────────────
def test_urls():
    section("۵. URL Configuration")
    from django.urls import reverse, NoReverseMatch
    from django.test import Client

    common_names = [
        "admin:index",
        "admin:login",
        "admin:logout",
        "admin:password_change",
        "admin:jsi18n",
    ]

    for name in common_names:
        try:
            url = reverse(name)
            ok(f"URL '{name}' → {url}")
        except NoReverseMatch:
            warn(f"URL '{name}' تعریف نشده است")
        except Exception as e:
            fail(f"URL '{name}' خطا", str(e))


# ── ۶. تست Settings ───────────────────────────────────────────────────────────
def test_settings():
    section("۶. تنظیمات Django (Settings)")
    from django.conf import settings

    checks = {
        "SECRET_KEY": lambda v: len(v) >= 20,
        "INSTALLED_APPS": lambda v: bool(v),
        "DATABASES": lambda v: bool(v),
        "STATIC_URL": lambda v: bool(v),
    }

    for key, validator in checks.items():
        try:
            val = getattr(settings, key)
            if validator(val):
                ok(f"{key} تنظیم شده است")
            else:
                warn(f"{key} مقدار ضعیفی دارد: {val!r}")
        except AttributeError:
            fail(f"{key} در settings موجود نیست")

    # DEBUG چک
    if getattr(settings, "DEBUG", None) is True:
        warn("DEBUG=True است — برای production غیرفعال کن")
    else:
        ok("DEBUG=False (آماده production)")

    # ALLOWED_HOSTS
    allowed = getattr(settings, "ALLOWED_HOSTS", [])
    if not allowed:
        warn("ALLOWED_HOSTS خالی است")
    else:
        ok(f"ALLOWED_HOSTS: {allowed}")


# ── ۷. تست System Check جنگو ──────────────────────────────────────────────────
def test_system_checks():
    section("۷. Django System Checks")
    from django.core import checks
    from django.test.utils import setup_test_environment

    try:
        setup_test_environment()
    except Exception:
        pass

    try:
        errors = checks.run_checks()
        critical = [e for e in errors if e.level >= checks.ERROR]
        warnings_ = [e for e in errors if e.level == checks.WARNING]

        if not errors:
            ok("هیچ خطا یا هشداری در system check نیست")
        else:
            for w in warnings_:
                warn(f"WARNING [{w.id}]: {w.msg}")
            for e in critical:
                fail(f"ERROR [{e.id}]: {e.msg}")
    except Exception as e:
        fail("system check شکست خورد", str(e))


# ── ۸. تست Static Files ───────────────────────────────────────────────────────
def test_static():
    section("۸. Static Files")
    from django.conf import settings

    static_root = getattr(settings, "STATIC_ROOT", None)
    static_url  = getattr(settings, "STATIC_URL", None)

    if static_url:
        ok(f"STATIC_URL = {static_url}")
    else:
        warn("STATIC_URL تنظیم نشده")

    if static_root:
        if os.path.exists(static_root):
            ok(f"STATIC_ROOT وجود دارد: {static_root}")
        else:
            warn(f"STATIC_ROOT وجود ندارد: {static_root} — collectstatic اجرا نشده؟")
    else:
        warn("STATIC_ROOT تنظیم نشده")


# ── گزارش نهایی ───────────────────────────────────────────────────────────────
def print_summary():
    total = len(passed) + len(failed)
    print(f"\n{BOLD}{'═'*55}{RESET}")
    print(f"{BOLD}  📋 خلاصه نتایج{RESET}")
    print(f"{'═'*55}")
    print(f"  {GREEN}✔ موفق:   {len(passed)}{RESET}")
    print(f"  {RED}✘ ناموفق: {len(failed)}{RESET}")
    print(f"  {YELLOW}⚠ هشدار:  {len(warnings)}{RESET}")
    print(f"  مجموع:    {total}")
    print(f"{'═'*55}")

    if failed:
        print(f"\n{RED}{BOLD}  ❌ موارد ناموفق:{RESET}")
        for f in failed:
            print(f"  {RED}• {f}{RESET}")

    if not failed:
        print(f"\n{GREEN}{BOLD}  🎉 پروژه بدون خطای بحرانی است!{RESET}")
    else:
        print(f"\n{RED}{BOLD}  ⛔ {len(failed)} خطا نیاز به بررسی دارد.{RESET}")


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Django Full Test Script")
    parser.add_argument(
        "--settings",
        help="مسیر settings (مثلاً: myproject.settings.local)",
        default=None,
    )
    args = parser.parse_args()

    # اضافه کردن مسیر پروژه به Python path
    sys.path.insert(0, os.getcwd())

    print(f"\n{BOLD}{CYAN}  🚀 Django Project & Admin Full Test{RESET}")
    print(f"  پروژه: {os.getcwd()}\n")

    setup_django(args.settings)
    test_database()
    test_migrations()
    test_settings()
    test_system_checks()
    test_static()
    test_urls()
    test_admin_panel()   # این باید آخر باشه چون یوزر موقت می‌سازه
    print_summary()