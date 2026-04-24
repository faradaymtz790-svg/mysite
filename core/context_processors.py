# core/context_processors.py

from .models import Notification  # <--- ADD THIS LINE

def notification_count(request):
    if request.user.is_authenticated:
        # Using 'timestamp' as we discovered in the previous error
        notifs = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        return {
            'unread_notifications_count': notifs.filter(is_read=False).count(),
            'recent_notifications': notifs[:5]
        }
    return {}