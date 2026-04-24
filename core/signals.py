from django.db.models.signals import post_save
from django.dispatch import receiver
# Change PostLike to PostLikes
from .models import Follow, PostLikes, Comment, Notification

# 1. Someone Followed You
@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type='follow',
            text="started following you."
        )

# 2. Someone Liked your Post
# core/signals.py
from .models import Notification

def notify_post_like(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.user, # The person who owns the post
            sender=instance.user,         # The person who liked it
            notification_type='post_like',
            post=instance.post,
            text="liked your post."
        )
# 3. Someone Commented or Replied
@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created:
        if instance.parent: # It's a reply
            Notification.objects.create(
                recipient=instance.parent.user,
                sender=instance.user,
                post=instance.post,
                notification_type='reply',
                text="replied to your comment."
            )
        else: # It's a top-level comment
            Notification.objects.create(
                recipient=instance.post.user,
                sender=instance.user,
                post=instance.post,
                notification_type='comment',
                text="commented on your post."
            )