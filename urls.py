"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from core import views  # ✅ Fixed: Ensure this points to 'core'
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from core import views 
from core.views import my_profile_redirect

# 🔹 NON-language URLs (Must stay outside i18n_patterns)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

# 🔹 LANGUAGE URLs (Wrapped in i18n_patterns)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    
    path('rosetta/', include('rosetta.urls')),
    path('accounts/', include('allauth.urls')),

    
    path('', views.home_view, name='root'),

    from django.views.generic import RedirectView

# Inside your urlpatterns...
path('', RedirectView.as_view(pattern_name='signup', permanent=False)),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    
    path('report/<int:post_id>/', views.report_post_view, name='report_post'),
    path('block-user/<int:user_id>/', views.toggle_block_user, name='toggle_block_user'),
    path('profile/', my_profile_redirect, name='profile_redirect'),
    path('niche-selection/', views.niche_selection, name='niche_selection'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    
    path('record-replay/<int:post_id>/', views.record_replay, name='record_replay'),
    path('record-listener/<int:post_id>/', views.record_listener, name='record_listener'),
    path('help/', views.help_center, name='help_center'),
    path('search/', views.search, name='search'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('notification/<int:notification_id>/click/', views.click_notification, name='click_notification'),

    path('follow/<str:username>/', views.follow_user, name='follow'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('create_post/', views.create_post, name='create_post'),
    path('feed/', views.posts_feed, name='feed'),
    path('like-post/<int:post_id>/', views.like_post),
    path('track-listener/<int:post_id>/', views.track_listener),
    path('following/<int:user_id>/', views.following_list, name='following_list'),
    path('followers/<int:user_id>/', views.followers_list, name='followers_list'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/', views.mark_notifications_read, name='mark_read'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('delete-post/<int:id>/', views.delete_post),
    # Make sure the name is exactly 'post_comments'
path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),

    # ⚙️ SETTINGS SECTION
    path('settings/', views.settings_view, name='settings'),
    path('settings/accounts/', views.delete_account, name='delete_account'),
    path('settings/account/', views.account_view, name='account'),
    path('settings/language/', views.language, name='language'),
    path('settings/privacy/', views.privacy, name='privacy'),
    path('settings/terms/', views.terms, name='terms'),
    path('settings/faqs/', views.faqs, name='faqs'),
    path('settings/help/', views.help_page, name='help'),
    path('settings/about/', views.about, name='about'),
    path('settings/invite/', views.invite, name='invite'),
    path('robot-check/', views.robot_check_view, name='robot_check'),
    
    prefix_default_language=False  
)

# 🔹 MEDIA FILES
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)