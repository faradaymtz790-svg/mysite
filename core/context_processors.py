def notification_count(request):
    if request.user.is_authenticated:
        notifs = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        return {
            'unread_notifications_count': notifs.filter(is_read=False).count(),
            'recent_notifications': notifs[:5]
        }
    # Return defaults for guests
    return {
        'unread_notifications_count': 0,
        'recent_notifications': []
    }