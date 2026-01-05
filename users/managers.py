from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        ایجاد کاربر عادی با شماره موبایل
        """
        if not phone_number:
            raise ValueError("شماره تلفن الزامی است")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        ایجاد سوپرکاربر
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("سوپرکاربر باید is_staff=True باشد")
        if not extra_fields.get("is_superuser"):
            raise ValueError("سوپرکاربر باید is_superuser=True باشد")

        return self.create_user(phone_number, password, **extra_fields)
