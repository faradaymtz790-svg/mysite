
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.i18n import i18n_patterns
from core import views

from core.views import my_profile_redirect # Ensure this is imported
# Also, ensure 'my_profile_redirect' is imported or defined
# If it is in views, use 'views.my_profile_redirect'



urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
     
    path('serviceworker.js', TemplateView.as_view(
        template_name="js/serviceworker.js",
        content_type='application/javascript'
    ), name='serviceworker'),

    path('manifest.json', TemplateView.as_view(
        template_name="manifest.json",
        content_type='application/json'
    ), name='manifest'),

    path('favicon.ico', RedirectView.as_view(
        url=settings.STATIC_URL + 'favicon.ico'
    )),

    
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('accounts/', include('allauth.urls')),

    # HOME (KEEP ONLY ONE)
    path('', views.home_view, name='home'),

    path('feed/', views.posts_feed, name='feed'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('niche-selection/', views.niche_selection, name='niche_selection'),

    # PROFILE
    path('profile/', my_profile_redirect, name='profile_redirect'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow'),
    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),
    path('profile/<str:username>/following/', views.following_list, name='following_list'),

    # POSTS
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),
    path('create_post/', views.create_post, name='create_post'),
    path('delete-post/<int:id>/', views.delete_post, name='delete_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),

    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    # TRACKING
    path('record-replay/<int:post_id>/', views.record_replay, name='record_replay'),
    path('record-listener/<int:post_id>/', views.record_listener, name='record_listener'),
    path('track-listener/<int:post_id>/', views.track_listener),

    # NOTIFICATIONS
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/', views.mark_notifications_read, name='mark_read'),
    path('notification/<int:notification_id>/click/', views.click_notification, name='click_notification'),
    path('search/', views.search, name='search'),

 
    path("audio-feed/", views.audio_call_feed, name="audio_feed"),
    path("start-audio-call/", views.start_audio_call, name="start_audio_call"),
    path("like-audio-call/<int:post_id>/", views.like_audio_call, name="like_audio_call"),
    path("track-audio-listener/<int:post_id>/", views.track_listener, name="track_listener"),
    path("delete-audio-call/<int:post_id>/", views.delete_audio_call, name="delete_audio_call"),

    path("call/", views.call_page, name="call"),
    path("user-search/", views.user_search, name="user_search"),
    path("save-call/", views.save_call, name="save_call"),
    path("post-call/", views.post_call, name="post_call"),
    path("call/accept/<int:call_id>/", views.accept_call, name="accept_call"),
path("call/decline/<int:call_id>/", views.decline_call, name="decline_call"),
    
    # SETTINGS
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
    path('help/', views.help_center, name='help_center'),

    # SAFETY
    path('report/<int:post_id>/', views.report_post_view, name='report_post'),
    path('block-user/<int:user_id>/', views.toggle_block_user, name='toggle_block_user'),
    path('robot-check/', views.robot_check_view, name='robot_check'),

    prefix_default_language=True
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)