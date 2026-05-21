from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Models ---
from django.db import models
from django.contrib.auth.models import User

# --- Profile ---

from django.db import models
from django.conf import settings  # <--- THIS IS REQUIRED
from django.contrib.auth.models import User


from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    image = CloudinaryField(
        'image',
        folder='profile_pics',
        blank=True,
        null=True,
        max_length=500
    )

    cover_photo = CloudinaryField(
        'image',
        folder='cover_photos',
        blank=True,
        null=True,
        max_length=500
    )

    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    links = models.URLField(max_length=500, blank=True)

    niches = models.JSONField(default=list, blank=True)

    blocked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='blocked_by',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



# ... Your Report model remains below ...


# --- Post ---
# --- Post ---





class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, default="Untitled Log")

    # Use CloudinaryField instead of CharField
    # 'auto' resource_type allows Cloudinary to detect if it's an image or audio
    image = CloudinaryField('image', null=True, blank=True)
    audio = CloudinaryField('auto', resource_type='auto', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    listeners_count = models.PositiveIntegerField(default=0)
    replays_count = models.PositiveIntegerField(default=0)
    
    played_by = models.ManyToManyField(User, related_name="played_posts", blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, through='PostLikes')

    def __str__(self):
        return f"{self.user.username} - {self.title[:20]}"


# --- PostLikes (M2M table) ---
class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This prevents a user from liking the same post multiple times
        unique_together = ('user', 'post')

# --- Follow ---
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower} follows {self.following}"


# --- Comment ---



# ... other models like Post ...

from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    # The types you requested
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('post_like', 'Post Like'),
        ('comment', 'Comment'),
        ('comment_like', 'Comment Like'),
        ('reply', 'Reply'),
        ('share', 'Share'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.recipient} ({self.notification_type})"




# Line 116
class Comment(models.Model):
    # Line 117 - MAKE SURE THIS IS INDENTED!
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=True, null=True)
    audio_comment = models.FileField(upload_to='comment_audios/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # These are the fields we added for likes and replies
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    

    

class HelpCenter(models.Model):
    # Field names match the data labels you're using
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    issue = models.TextField(max_length=350)
    
    # Tracking data
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Help Request from {self.full_name} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        # This makes it look professional in the Django Admin
        verbose_name = "Help Center Entry"
        verbose_name_plural = "Help Center Entries"
        ordering = ['-created_at']


        

class Block(models.Model):
    # If you also have a Block model, ensure its related_name is unique
    blocked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='block_entries', # Ensure this is also unique
        blank=True
    )


class Report(models.Model):
    # Ensure this uses AUTH_USER_MODEL as well for consistency
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    reason = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)





class RadioPost(models.Model):

    channel = models.ForeignKey(
        RadioChannel,
        on_delete=models.CASCADE,
        related_name='radio_posts'
    )

    topic = models.CharField(max_length=255)

    title = models.CharField(max_length=255)

    audio_file = models.FileField(
        upload_to='radio_audio/'
    )

    background_image = models.ImageField(
        upload_to='radio_background_images/',
        blank=True,
        null=True
    )

    background_video = models.FileField(
        upload_to='radio_background_videos/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    listeners_count = models.PositiveIntegerField(
        default=0
    )

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return self.title


class RadioLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        RadioPost,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'post')


class RadioComment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        RadioPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class RadioSubscriber(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    channel = models.ForeignKey(
        RadioChannel,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'channel')

    def __str__(self):
        return f"{self.user.username} subscribed to {self.channel.channel_name}"



    class RadioChannel(models.Model):
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    channel_name = models.CharField(max_length=100)

    profile_image = models.ImageField(
        upload_to='radio_channel_profiles/',
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    owner_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    topics = models.CharField(
        max_length=150
    )

    frequency = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    spotify_link = models.URLField(
        blank=True,
        null=True
    )

    youtube_link = models.URLField(
        blank=True,
        null=True
    )

    schedule = models.TextField()

    email = models.EmailField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.channel_name