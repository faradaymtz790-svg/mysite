from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# =========================
# PROFILE
# =========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    links = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover/', blank=True, null=True)

    niches = models.JSONField(default=list, blank=True)

    blocked_users = models.ManyToManyField(
        User,
        related_name='blocked_by',
        blank=True
    )

    def __str__(self):
        return self.user.username


# =========================
# POST
# =========================
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts/')
    audio = models.FileField(upload_to='audio_posts/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(User, through='PostLikes', related_name='liked_posts')

    replays_count = models.PositiveIntegerField(default=0)
    listeners_count = models.PositiveIntegerField(default=0)

    played_by = models.ManyToManyField(User, related_name='played_posts', blank=True)

    def __str__(self):
        return self.title


class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


# =========================
# FOLLOW SYSTEM
# =========================
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')


# =========================
# COMMENTS
# =========================
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    title = models.TextField()
    audio_comment = models.FileField(upload_to='comment_audio/', blank=True, null=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.title[:30]}"


# =========================
# NOTIFICATIONS
# =========================
class Notification(models.Model):
    NOTIF_TYPES = [
        ('follow', 'Follow'),
        ('post_like', 'Post Like'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
        ('like', 'Comment Like'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')

    notification_type = models.CharField(max_length=20, choices=NOTIF_TYPES)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    text = models.TextField()

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


# =========================
# REPORTS
# =========================
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    reason = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class Block(models.Model):
    blocker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocking'
    )

    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_by_users'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')
        indexes = [
            models.Index(fields=['blocker']),
            models.Index(fields=['blocked']),
        ]

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
# =========================
# AUDIO CALL POSTS
# =========================
class AudioCallPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    heading = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    audio_file = models.FileField(upload_to='audio_calls/')
    cover_image = models.ImageField(upload_to='audio_calls/cover/', blank=True, null=True)
    cover_video = models.FileField(upload_to='audio_calls/video/', blank=True, null=True)
    background_music = models.FileField(upload_to='audio_calls/music/', blank=True, null=True)

    duration_minutes = models.IntegerField(default=0)

    likes = models.ManyToManyField(User, related_name='liked_audio_calls', blank=True)
    listeners = models.ManyToManyField(User, related_name='audio_call_listeners', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


# =========================
# CALL SYSTEM
# =========================
class CallSession(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_calls')
    participants = models.ManyToManyField(User, related_name='call_participations', blank=True)

    heading = models.CharField(max_length=255, blank=True, null=True)
    duration_seconds = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class CallPost(models.Model):
    call = models.ForeignKey(CallSession, on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)



 class AudioCall(models.Model):
    caller = models.ForeignKey(User, related_name="sent_calls", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_calls", on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=[
            ("ringing", "Ringing"),
            ("accepted", "Accepted"),
            ("declined", "Declined"),
            ("ended", "Ended"),
        ],
        default="ringing"
    )

    created_at = models.DateTimeField(auto_now_add=True)   