import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import Follow, PostLikes, Comment, Notification

# ==========================================
# 1. NEW SIGNUP REDIRECTION FLAG
# ==========================================
@receiver(user_signed_up)
def mark_new_signup(request, user, **kwargs):
    """
    Places a temporary flag inside the session data.
    The ZeedAccountAdapter will read this flag and route to /niche_selection/.
    """
    request.session['new_signup_redirect'] = True


# ==========================================
# 2. SOCIAL NOTIFICATIONS
# ==========================================

# --- Someone Followed You ---
@receiver(post_save, sender=Follow)
def notify_follow(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type='follow',
            text="started following you."
        )


# --- Someone Liked Your Post (FIXED DECORATOR & SELF-LIKE) ---
@receiver(post_save, sender=PostLikes)
def notify_post_like(sender, instance, created, **kwargs):
    if created:
        # Avoid notifying if someone likes their own post
        if instance.post.user != instance.user:
            Notification.objects.create(
                recipient=instance.post.user, # The person who owns the post
                sender=instance.user,         # The person who liked it
                notification_type='post_like',
                post=instance.post,
                text="liked your post."
            )


# --- Someone Commented or Replied (FIXED SELF-COMMENTING) ---
@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created:
        # Determine if the comment is audio-based or text-based
        is_audio = hasattr(instance, 'audio_comment') and instance.audio_comment
        verb = "sent an audio comment" if is_audio else "commented"

        if instance.parent:  # It's a reply to a comment
            # Avoid notifying if someone replies to their own comment
            if instance.parent.user != instance.user:
                Notification.objects.create(
                    recipient=instance.parent.user,
                    sender=instance.user,
                    post=instance.post,
                    comment=instance, 
                    notification_type='reply',
                    text=f"{verb} on your comment."
                )
        else:  # It's a top-level comment on a post
            # Avoid notifying if someone comments on their own post
            if instance.post.user != instance.user:
                Notification.objects.create(
                    recipient=instance.post.user,
                    sender=instance.user,
                    post=instance.post,
                    comment=instance,
                    notification_type='comment',
                    text=f"{verb} on your post."
                )