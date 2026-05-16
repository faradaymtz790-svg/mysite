import logging
logger = logging.getLogger(__name__)

import time
import random
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext as _

from .models import Post, Follow, Comment, Notification, PostLikes
from .forms import CommentForm


import cloudinary.uploader


# This line must be at the very far left (no spaces)

 # Use 'core' (or whatever your app name is)

# =========================
# BASIC PAGES
# =========================

def home_view(request):
    # Just show the page, don't redirect here!
    return render(request, 'home.html')

@login_required
def language(request):
    return render(request, 'language.html')

@login_required
def privacy(request):
    return render(request, 'privacy.html')

@login_required
def terms(request):
    return render(request, 'terms.html')

@login_required
def faqs(request):
    return render(request, 'faqs.html')

@login_required
def help_page(request):
    return render(request, 'help.html')

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def invite(request):
    return render(request, 'invite_friend.html')

@login_required
def settings_view(request):
    return render(request, 'settings.html')

@login_required
def account_view(request):
    return render(request, 'account.html')


# =========================
# AUTH
# =========================

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages


# from ratelimit.decorators import ratelimit # Uncomment if you install django-ratelimit

# @ratelimit(key='ip', rate='3/15m', block=True) # Optional: prevents brute force


import time
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login



def signup(request):
    if request.method == 'POST':

        # --- 1. SECURITY CHECKS (Honeypot, Time, CAPTCHA) ---

        # Honeypot (bot trap)
        if request.POST.get('company_name_extra'):
            return redirect('signup')

        # Time check
        load_time = request.POST.get('form_load_time')

        try:
            submit_time = int(time.time())

            if load_time:
                if submit_time - int(load_time) < 4:
                    messages.error(request, "Form submitted too quickly. Are you a bot?")
                    return redirect('signup')

        except (ValueError, TypeError):
            return redirect('signup')

        # CAPTCHA (SAFE VERSION)
        try:
            user_answer = request.POST.get('captcha_answer')
            correct_answer = request.session.get('captcha_result')

            if correct_answer is None:
                messages.error(request, "Captcha expired. Please try again.")
                return redirect('signup')

            if user_answer is None:
                messages.error(request, "Please answer the captcha.")
                return redirect('signup')

            if int(user_answer) != int(correct_answer):
                messages.error(request, "Incorrect math answer. Please try again.")
                return redirect('signup')

        except (ValueError, TypeError):
            messages.error(request, "Invalid captcha input.")
            return redirect('signup')

        # --- 2. DATA CAPTURE ---
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        # --- 3. VALIDATION ---
        if not username or not email or not password or not confirm:
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        # --- 4. CREATE USER ---
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Clean session safely
            request.session.pop('captcha_result', None)

            # LOGIN USER (SAFE)
            login(request, user)

            return redirect('niche_selection')

        except Exception as e:
            messages.error(request, f"Signup failed: {e}")
            return redirect('signup')

    # --- GET REQUEST (LOAD FORM) ---
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    request.session['captcha_result'] = num1 + num2

    return render(request, 'signup.html', {
        'num1': num1,
        'num2': num2
    })





# =========================
# PROFILE
# =========================


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required  # Added missing import
from django.contrib.auth.models import User
from .models import Profile, Post, Follow

@login_required
def profile_view(request, username=None):
    # 1. Determine which user we are looking at
    if username:
        viewed_user = get_object_or_404(User, username=username)
    else:
        # Guaranteed to be authenticated because of @login_required decorator
        viewed_user = request.user

    # 2. Get or create the profile
    profile, created = Profile.objects.get_or_create(user=viewed_user)
    
    # 3. Get posts for the viewed user
    user_posts = Post.objects.filter(user=viewed_user).order_by('-created_at')
    
    # 4. Calculate totals for replays and listeners
    total_replays = user_posts.aggregate(Sum('replays_count'))['replays_count__sum'] or 0
    total_listeners = user_posts.aggregate(Sum('listeners_count'))['listeners_count__sum'] or 0

    # 5. Check follow status
    is_following = False
    if request.user != viewed_user:
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=viewed_user
        ).exists()

    # 6. Calculate Follower/Following counts
    followers_count = Follow.objects.filter(following=viewed_user).count()
    following_count = Follow.objects.filter(follower=viewed_user).count()

    # 7. Final Context and Render
    context = {
        'profile': profile,
        'user_posts': user_posts,
        'total_replays': total_replays,
        'total_listeners': total_listeners,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    
    return render(request, 'profile.html', context)



# =========================
# NICHES
# =========================


# =========================
# POSTS
# =========================

from django.shortcuts import render, redirect

def home_landing_view(request):
    # 1. If the user is already logged in, skip the welcome page completely
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
        
    # 2. If they are a guest, show them your beautiful welcoming page
    return render(request, 'home.html')

# ... your other views like profile_view or post_comments ...


@login_required
def posts_feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts_feed.html', {'posts': posts})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, PostLikes, Notification

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user already liked this post
    like_qs = PostLikes.objects.filter(user=request.user, post=post)

    if like_qs.exists():
        # If they already liked it, clicking again removes the like (Unlike)
        like_qs.delete()
        liked = False
    else:
        # Create the like record
        PostLikes.objects.create(user=request.user, post=post)
        liked = True
        
        # --- NOTIFICATION LOGIC ---
        # Only notify the owner if someone ELSE likes their post
        if request.user != post.user:
            Notification.objects.create(
                recipient=post.user,           # Matches 'recipient' in models.py
                sender=request.user,           # Matches 'sender' in models.py
                notification_type='post_like', # Matches choices in models.py
                post=post,                     # Links to the specific post
                text=f"liked your post: {post.title[:30]}" # Matches 'text' in models.py
            )
        # --- END NOTIFICATION LOGIC ---
    
    return JsonResponse({
        'liked': liked,
        'count': post.likes.count()
    })




def track_listener(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 👂 Update the Ear (Total Replays)
    post.replays_count += 1 
    
    # 🎧 Update the Headphones (Unique Listeners)
    if request.user.is_authenticated:
        if not post.played_by.filter(id=request.user.id).exists():
            post.played_by.add(request.user)
            post.listeners_count += 1
    
    # THIS IS THE MOST IMPORTANT LINE
    post.save() 
    
    return JsonResponse({
        'total_plays': post.replays_count,
        'unique_listeners': post.listeners_count
    })


# =========================
# FOLLOW
# =========================

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Follow # Ensure this is your Follow model

User = get_user_model()
@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return JsonResponse({'error': 'You cannot follow yourself'}, status=400)

    is_blocked = (
        request.user.profile.blocked_users.filter(username=target_user.username).exists() or
        target_user.profile.blocked_users.filter(username=request.user.username).exists()
    )
    
    if is_blocked:
        return JsonResponse({'error': 'Action not allowed: Blocked relationship exists'}, status=403)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        # If they already followed them, remove it (Unfollow)
        follow.delete()
        status = 'unfollowed'
        
        # Optional cleanup: Delete the notification record if they unfollow right away
        Notification.objects.filter(
            sender=request.user, 
            recipient=target_user, 
            notification_type='follow'
        ).delete()
    else:
        status = 'followed'
        
        # --- NEW FOLLOW NOTIFICATION TRIGGER ---
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow',
            text="started following you."
        )
        # --- END NOTIFICATION TRIGGER ---

    followers_count = Follow.objects.filter(following=target_user).count()

    return JsonResponse({
        'status': status, 
        'followers_count': followers_count
    })




 # Assuming your model is named Follow

# Ensure your Follow model is imported

def followers_list(request, username):
    # 1. Get the user object using the USERNAME from the URL
    profile_user = get_object_or_404(User, username=username)
    
    # 2. Filter the Follow model where 'following' is this user
    # This gets everyone who is following this specific user
    followers = Follow.objects.filter(following=profile_user)

    return render(request, 'followers.html', {
        'followers': followers,
        'profile_user': profile_user
    })


def following_list(request, username):
    # Lookup by username instead of ID
    viewed_user = get_object_or_404(User, username=username)
    following = Follow.objects.filter(follower=viewed_user)
    return render(request, 'following.html', {'viewed_user': viewed_user, 'following': following})

 # Redirect back to the same page to see the new comment
  

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Post, Comment, Notification
@login_required
def post_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        text_data = request.POST.get('title') 
        audio_data = request.FILES.get('audio_comment')
        parent_id = request.POST.get('parent_id')
        
        # 1. Save the comment
        new_comment = Comment.objects.create(
            user=request.user,
            post=post,
            title=text_data,
            audio_comment=audio_data,
            parent_id=parent_id if parent_id else None
        )

        # 2. Notification Logic
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
                # Only notify if you are replying to someone else
                if request.user != parent_comment.user:
                    Notification.objects.create(
                        recipient=parent_comment.user, 
                        sender=request.user,
                        notification_type='reply',  # FIX 1: Set type to 'reply' instead of 'comment'
                        post=post,
                        comment=new_comment,        # FIX 2: Links the comment instance object
                        text=f"replied to your comment: {text_data[:20]}"
                    )
            except Comment.DoesNotExist:
                pass # Parent comment was likely deleted
        
        # Notify Post Owner (if they aren't the one commenting)
        elif request.user != post.user:
            Notification.objects.create(
                recipient=post.user,
                sender=request.user,
                notification_type='comment',
                post=post,
                comment=new_comment,            # FIX 3: Links the comment instance object
                text=f"commented on your post: {text_data[:20]}"
            )
        
        return redirect('post_comments', post_id=post.id)

    # 3. GET Logic (Optimized Query)
    comments = Comment.objects.filter(post=post, parent=None)\
                              .select_related('user', 'user__profile')\
                              .order_by('-created_at')
                              
    return render(request, 'comments.html', {
        'post': post, 
        'comments': comments
    })



@login_required
@require_POST
def delete_comment(request, comment_id):
    """
    Deletes a comment via an AJAX POST request.
    Ensures that only the comment author (or an admin) can delete it.
    """
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check ownership or admin status
    if comment.user == request.user or request.user.is_staff:
        comment.delete()
        return JsonResponse({'status': 'success', 'message': 'Comment deleted successfully.'})
    
    return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)




# NOTIFICATIONS
# =========================
# @login_required  <-- Add a '#' to the start of this line


# =========================
# SEARCH
# =========================

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Post

def search(request):
    query = request.GET.get('q', '').strip()
    user_results = []
    post_results = []

    if query:
        # 1. Search for users by username
        user_results = User.objects.filter(username__icontains=query)

        # 2. Search for posts by title words
        post_results = Post.objects.filter(Q(title__icontains=query))

    return render(request, 'search_results.html', {
        'query': query,
        'user_results': user_results,
        'post_results': post_results,
    })


import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

# Define the logger so it doesn't crash
logger = logging.getLogger(__name__)


# Add this import at the top



import cloudinary.uploader
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post


from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Post

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image')
        audio_file = request.FILES.get('audio')

        if not image_file:
            # If AJAX, return JSON. If standard form, return HTML.
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Please select an image.'}, status=400)
            return render(request, 'create_post.html', {'error': 'Please select an image.'})

        try:
            new_post = Post(
                user=request.user,
                title=title,
                image=image_file,
                audio=audio_file
            )
            new_post.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'})
            return redirect('feed')

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': str(e)}, status=500)
            return render(request, 'create_post.html', {'error': f"Upload failed: {str(e)}"})

    return render(request, 'create_post.html')


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request):
    profile = request.user.profile
    
    if request.method == "POST":
        profile.bio = request.POST.get('bio', profile.bio)
        profile.location = request.POST.get('location', profile.location)
        profile.links = request.POST.get('links', profile.links)

        image = request.FILES.get('image')
        if image:
            # Note: Cloudinary handles deletion via the public_id usually, 
            # but this is fine for standard storage
            profile.image = image

        cover = request.FILES.get('cover_photo')
        if cover:
            profile.cover_photo = cover

        profile.save()
        
        # If using AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        
        # If using a standard form, redirect back to profile
        return redirect('profile', username=request.user.username)

    # Handle GET request: Show the edit form
    return render(request, 'core/update_profile.html', {'profile': profile})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def delete_post(request, id):
    # Only allow POST requests for deletion
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Use get_object_or_404 to handle invalid IDs gracefully
    post = get_object_or_404(Post, id=id)

    # Verify ownership
    if request.user != post.user:
        return JsonResponse({"error": "You are not authorized to delete this post."}, status=403)

    # Perform the deletion
    post.delete()
    
    return JsonResponse({"success": True, "message": "Post deleted successfully"})


    

# ✅ CORRECT: The return must be "inside" the function block
def settings_view(request):
    return render(request, 'settings.html')


# Do this for the rest (language, faqs, etc.)


@login_required
def invite(request):
    # This passes the logged-in user to the template 
    # so the referral link works: {{ user.username }}
    return render(request, 'invite.html')



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user in request.user.following.all():
        request.user.following.remove(target_user)
        status = 'unfollowed'
    else:
        request.user.following.add(target_user)
        status = 'followed'
        
    return JsonResponse({
        'status': status,
        # THIS KEY MUST MATCH THE JS BELOW
        'followers_count': target_user.followers.count(), 
    })



# core/views.py


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    
    # This specifically targets the existing relationship and deletes it
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
        
    return redirect('profile', username=username)




def record_replay(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.replays_count += 1  # EAR icon: always increases
        post.save()
        return JsonResponse({'new_replay_count': post.replays_count})

def record_listener(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        # HEADPHONE icon: logic to check if user already listened
        # For testing, we just increment it.
        post.listeners_count += 1 
        post.save()
        return JsonResponse({'new_listener_count': post.listeners_count})
    



def help_center(request):
    if request.method == 'POST':
        name = request.POST.get('userName')
        email = request.POST.get('userEmail')
        issue = request.POST.get('userIssue')

        # Backend Security: Validate lengths
        if len(name) > 100 or len(email) > 100 or len(issue) > 350:
            messages.error(request, "Input exceeds character limits.")
            return redirect('help_center')

        # Logic: Send an email to the founder or save to Database
        # send_mail(f"New Support Ticket from {name}", issue, email, ['faradaymwambe@gmail.com'])

        messages.success(request, "Thanks for your feedback! We are working on it.")
        return redirect('home')

    return render(request, 'help.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Delete the user first
        # logout(request)  <- You don't actually need this if the user is deleted
        return redirect('home') 
    
    # Ensure this path matches exactly where your file is located
    return render(request, 'settings/accounts.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def notifications(request):
    # Optimized using select_related so templates can read post/comment/sender info instantly
    user_notifications = Notification.objects.filter(recipient=request.user)\
                                           .select_related('sender', 'sender__profile', 'post', 'comment')\
                                           .order_by('-timestamp')
                                           
    unread_count = user_notifications.filter(is_read=False).count()
    
    return render(request, 'notifications.html', {
        'notifications': user_notifications,
        'unread_count': unread_count
    })


@login_required
def click_notification(request, notification_id):
    """
    Marks a notification as read and routes the user to the specific content.
    """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    
    notification.is_read = True
    notification.save()

    # --- ROUTING LOGIC ---

    # 1. FOLLOW: Go to the profile of the person who followed you
    if notification.notification_type == 'follow':
        return redirect('profile', username=notification.sender.username)

    # 2. POST ACTIONS: (Likes, New Posts, Shares) -> Go to your comments page
    elif notification.notification_type in ['post_like', 'post_add', 'share']:
        if notification.post:
            return redirect('post_comments', post_id=notification.post.id)

    # 3. INTERACTION ACTIONS: (Comments, Replies, Comment Likes)
    elif notification.notification_type in ['comment', 'reply', 'comment_like']:
        # This checks if a specific sub-comment exists, and appends a CSS ID tag anchor 
        # so the screen automatically smooth-scrolls down to that explicit comment.
        if notification.comment and notification.post:
            return redirect(f'/post/{notification.post.id}/comments/#comment-{notification.comment.id}')
        elif notification.post:
            return redirect('post_comments', post_id=notification.post.id)

    # Default fallback
    return redirect('notifications')


def notification_count(request):
    """
    Context processor: Provides data to every page (like the navbar badge).
    """
    if request.user.is_authenticated:
        # Changed fields from '-created_at' to '-timestamp' to match your schema update
        notifs = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        return {
            'unread_notifications_count': notifs.filter(is_read=False).count(),
            'recent_notifications': notifs[:5]
        }
    return {}






@login_required
def mark_notifications_read(request, notification_id):
    """View to mark a single notification as read"""
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
    return redirect('notifications')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification  # This imports the model from models.py


# In views.py
from django.contrib.auth.decorators import login_required


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    # 1. Fetch comments specifically for this post
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    
    # 2. Check if current user likes this post (for the heart icon)
    is_liked = post.likes.filter(id=request.user.id).exists()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments, # Must be named 'comments' for the loop in HTML
        'is_liked': is_liked,
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification  # Adjust this import to match your app structure

@login_required
def notifications_view(request):
    # 1. Fetch all notifications for the current logged-in user
    notifications = Notification.objects.filter(recipient=request.user)\
                                      .select_related('sender', 'sender__profile', 'post', 'comment')\
                                      .order_by('-timestamp')
    
    # 2. Calculate dynamically how many are unread for the green badge counter
    unread_count = notifications.filter(is_read=False).count()

    # 3. Render the template with both the list and the unread count context variables
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })


def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    profile_data = Profile.objects.get(user=user_profile)
    
    # Check if the logged-in user is already following this person
    if request.user.is_authenticated:
        is_following = FollowerCount.objects.filter(follower=request.user.username, user=username).exists()
    else:
        is_following = False

    return render(request, 'profile.html', {
        'user_profile': user_profile,
        'profile_data': profile_data,
        'is_following': is_following,
    })



# core/views.py
from django.shortcuts import render, redirect
from .forms import SignupForm # Make sure this matches your form class

def robot_check_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # The library automatically validates the captcha here!
            request.session['robot_passed'] = True
            return redirect('signup') # Or wherever you want to go
    else:
        form = SignupForm()
    
    return render(request, 'robot_check.html', {'form': form})

# core/views.py
from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # If the captcha is valid, create the user!
            # ... your logic here
            return redirect('profile', username=user.username)
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})





from django.conf import settings
from django.http import HttpResponse

def debug_keys(request):
    return HttpResponse(f"Public Key: {settings.RECAPTCHA_PUBLIC_KEY}")



# In core/views.py



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Report

@login_required
def report_post_view(request, post_id):
    # Retrieve the specific post being reported
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        details = request.POST.get('details', '')
        
        # Create the report record
        Report.objects.create(
            user=request.user,
            post=post,
            reason=reason,
            description=details,
        )
        
        # Add success message for the user
        messages.success(request, "Report submitted successfully. We will work on it.")
        
        # Redirect to your home page or feed. 
        # Replace 'home' with the name you defined in your urls.py for your feed page.
        return redirect('feed') 
    
    # Render the standalone report page for GET requests
    return render(request, 'report_post.html', {'post': post})


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def toggle_block_user(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        profile = request.user.profile
        
        # Check if already blocked (to determine if we are unblocking)
        if target_user in profile.blocked_users.all():
            # UNBLOCKING
            profile.blocked_users.remove(target_user)
            is_blocked = False
        else:
            # BLOCKING
            profile.blocked_users.add(target_user)
            
            # Clean up follow relationships immediately upon blocking
            Follow.objects.filter(follower=request.user, following=target_user).delete()
            Follow.objects.filter(follower=target_user, following=request.user).delete()
            
            is_blocked = True
            
        return JsonResponse({'is_blocked': is_blocked})
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Inside your Profile model or a signal
# Inside your Profile model in models.py
def block_user(self, target_user):
    self.blocked_users.add(target_user)
    # Automatically clean up follows
    Follow.objects.filter(follower=self.user, following=target_user).delete()
    Follow.objects.filter(follower=target_user, following=self.user).delete()



from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Post, Report, Follow

User = get_user_model()

# 
@login_required
def feed_view(request):
    # --- START OF REPAIR CODE ---
    # Find the user with the space issue (like " in pocket")
    problem_user = User.objects.filter(username__contains=' ').first()
    if problem_user:
        # .strip() removes the leading/trailing spaces
        # .replace(' ', '_') turns middle spaces into underscores
        problem_user.username = problem_user.username.strip().replace(' ', '_')
        problem_user.save()
    # --- END OF REPAIR CODE ---

    # Your existing logic
    blocked_ids = list(request.user.profile.blocked_users.values_list('id', flat=True))
    blockers_ids = list(User.objects.filter(profile__blocked_users=request.user).values_list('id', flat=True))
    excluded_ids = blocked_ids + blockers_ids
    
    posts = Post.objects.exclude(user__id__in=excluded_ids).order_by('-created_at')
    
    return render(request, 'feed.html', {
        'posts': posts,
        'blocked_ids': excluded_ids 
    })


# In core/views.py
from django.shortcuts import redirect

def my_profile_redirect(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)
    return redirect('login')


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
import time

def login_view(request):
    if request.method == 'POST':
        # --- SECURITY CHECKS ---
        if request.POST.get('company_name_extra'):
            return redirect('login')

        load_time = request.POST.get('form_load_time')
        if load_time and (int(time.time()) - int(load_time) < 2):
            messages.error(request, "Submission too fast. Please try again.")
            return redirect('login')

        # --- LOGIN LOGIC ---
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Explicitly set the backend for compatibility with allauth
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # REDIRECT: Use the username to build the profile URL
                # This matches: path('profile/<str:username>/', views.profile, name='profile')
                return redirect('profile', username=user.username)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})




import json
from django.shortcuts import render, redirect
from django.contrib import messages


import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required  # This prevents the 'AnonymousUser' error
def niche_selection(request):
    if request.method == 'POST':
        # 1. Get the data from the form
        selected_niches_raw = request.POST.get('niches')
        
        if selected_niches_raw:
            try:
                # Convert the string from the frontend into a Python list
                niches_list = json.loads(selected_niches_raw)
                
                # Update or Create the profile for the logged-in user
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.niches = niches_list
                profile.save()
            except json.JSONDecodeError:
                # Handle case where 'niches' data is formatted incorrectly
                pass 

        # 2. Redirect using the authenticated user's session data
        # This fixes the 'NoReverseMatch' error by ensuring username is never empty
        return redirect('profile', username=request.user.username)

    # For a GET request, just show the page
    return render(request, 'niche_selection.html')



def account_view(request):
    return render(request, 'account.html')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment, Notification

@login_required
def like_comment(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user
        
        # Toggle the like status in the ManyToMany field
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
            liked = False
            
            # Clean up notification if they unlike the comment
            Notification.objects.filter(
                sender=user,
                recipient=comment.user,
                notification_type='comment_like',
                comment=comment
            ).delete()
        else:
            comment.likes.add(user)
            liked = True
            
            # Send a notification to the person who wrote the comment
            if user != comment.user:
                # SAFE CHECK: Get the post from the comment, or fall back to its parent's post if it's a reply
                associated_post = comment.post if comment.post else (comment.parent.post if comment.parent else None)

                Notification.objects.create(
                    recipient=comment.user, 
                    sender=user,            
                    notification_type='comment_like',
                    post=associated_post,    # Now handles replies safely!
                    comment=comment,         
                    text="liked your comment."
                )
                
        return JsonResponse({
            'liked': liked,
            'likes_count': comment.likes.count()
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
