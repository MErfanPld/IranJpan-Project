from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from users.models import User


class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label="شماره موبایل",
        max_length=11,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "شماره موبایل"
        })
    )
    password = forms.CharField(
        label="گذرواژه",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "گذرواژه"
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )


    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone_number")
        password = cleaned_data.get("password")

        user = authenticate(phone_number=phone, password=password)
        if not user:
            raise ValidationError("شماره موبایل یا گذرواژه نادرست است")

        if not user.is_active:
            raise ValidationError("حساب کاربری غیرفعال است")

        cleaned_data["user"] = user
        return cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label="گذرواژه",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "گذرواژه",
        })
    )
    password2 = forms.CharField(
        label="تکرار گذرواژه",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "تکرار گذرواژه",
        })
    )

    class Meta:
        model = User
        fields = ("phone_number", "email", "first_name", "last_name")
        widgets = {
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "شماره موبایل",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل (اختیاری)",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise ValidationError("گذرواژه‌ها یکسان نیستند")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
