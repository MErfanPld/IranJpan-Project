from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """فرم ارسال پیام"""
    
    class Meta:
        model = Message
        fields = ['message', 'image']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'پیام خود را بنویسید...',
                'rows': 3,
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        self.receiver = kwargs.pop('receiver', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.sender:
            instance.sender = self.sender
        if self.receiver:
            instance.receiver = self.receiver
        if commit:
            instance.save()
        return instance