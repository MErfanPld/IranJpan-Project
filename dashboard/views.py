from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Message
from .forms import MessageForm
from settings.models import SiteSettings


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["membership"] = getattr(self.request.user, "membership", None)
        context['site_settings'] = SiteSettings.objects.first()
        return context


class MessageListView(LoginRequiredMixin, ListView):
    """لیست پیام‌های کاربر"""
    
    model = Message
    template_name = 'dashboard/message_list.html'
    context_object_name = 'conversations'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        
        # اگر ادمین است، همه مکالمات را نشان بده
        if user.is_staff or user.is_superuser:
            # دریافت همه کاربرانی که با آن‌ها پیام رد و بدل شده
            sent_messages = Message.objects.values_list('receiver', flat=True)
            received_messages = Message.objects.values_list('sender', flat=True)
            
            # ترکیب و حذف تکراری‌ها
            user_ids = set(list(sent_messages) + list(received_messages))
            
            # بازگشت آخرین پیام با هر کاربر
            conversations = []
            for user_id in user_ids:
                # پیدا کردن آخرین پیام بین هر دو کاربر
                last_message = Message.objects.filter(
                    Q(sender_id=user_id) | Q(receiver_id=user_id)
                ).order_by('-created_at').first()
                if last_message:
                    conversations.append(last_message)
            
            return sorted(conversations, key=lambda x: x.created_at, reverse=True)
        
        # اگر کاربر عادی است، فقط پیام‌های خودش را نشان بده
        else:
            sent_messages = Message.objects.filter(sender=user).values_list('receiver', flat=True)
            received_messages = Message.objects.filter(receiver=user).values_list('sender', flat=True)
            
            # ترکیب و حذف تکراری‌ها
            user_ids = set(list(sent_messages) + list(received_messages))
            
            # بازگشت آخرین پیام با هر کاربر
            conversations = []
            for user_id in user_ids:
                last_message = Message.objects.filter(
                    Q(sender=user, receiver_id=user_id) | 
                    Q(sender_id=user_id, receiver=user)
                ).order_by('-created_at').first()
                if last_message:
                    conversations.append(last_message)
            
            return sorted(conversations, key=lambda x: x.created_at, reverse=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'صندوق پیام‌ها'
        context['is_admin'] = self.request.user.is_staff or self.request.user.is_superuser
        return context


class MessageDetailView(LoginRequiredMixin, ListView):
    """نمایش مکالمه با یک کاربر خاص"""
    
    model = Message
    template_name = 'dashboard/message_detail.html'
    context_object_name = 'messages'
    paginate_by = 50
    
    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs.get('user_id')
        
        # دریافت پیام‌های بین دو کاربر
        queryset = Message.objects.filter(
            Q(sender=user, receiver_id=other_user_id) | 
            Q(sender_id=other_user_id, receiver=user)
        ).order_by('created_at')
        
        # خوانده شدن پیام‌ها
        queryset.filter(receiver=user, is_read=False).update(is_read=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_user'] = get_object_or_404(
            self.request.user.__class__, 
            id=self.kwargs.get('user_id')
        )
        context['form'] = MessageForm()
        context['page_title'] = f'مکالمه با {context["other_user"].get_full_name()}'
        return context
    
    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver_id = self.kwargs.get('user_id')
            message.save()
            return redirect('dashboard:conversation', user_id=self.kwargs.get('user_id'))
        return self.get(request, *args, **kwargs)


class SendMessageView(LoginRequiredMixin, CreateView):
    """ارسال پیام جدید"""
    
    model = Message
    form_class = MessageForm
    template_name = 'dashboard/send_message.html'
    success_url = reverse_lazy('dashboard:list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['sender'] = self.request.user
        kwargs['receiver'] = get_object_or_404(
            self.request.user.__class__,
            id=self.kwargs.get('user_id')
        )
        return kwargs
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = get_object_or_404(
            self.request.user.__class__,
            id=self.kwargs.get('user_id')
        )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receiver'] = get_object_or_404(
            self.request.user.__class__,
            id=self.kwargs.get('user_id')
        )
        context['page_title'] = f'ارسال پیام به {context["receiver"].get_full_name()}'
        return context