from django.urls import path
from .views import DashboardView, MessageDetailView,MessageListView,SendMessageView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    
    # لیست صندوق پیام‌ها
    path('message/list/', MessageListView.as_view(), name='list'),
    
    # مکالمه با یک کاربر خاص
    path('message/conversation/<int:user_id>/', MessageDetailView.as_view(), name='conversation'),
    
    # ارسال پیام جدید
    path('message/send/<int:user_id>/', SendMessageView.as_view(), name='send'),
]
