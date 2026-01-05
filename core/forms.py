from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(
        label='جستجو',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجو..'
        })
    )



from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ایمیل'}),
            'phone_number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'تلفن'}),
            'subject': forms.TextInput(attrs={'class':'form-control', 'placeholder':'موضوع'}),
            'message': forms.Textarea(attrs={'class':'form-control', 'placeholder':'پیام خود را بنویسید', 'rows':6}),
        }