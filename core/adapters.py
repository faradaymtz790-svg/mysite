# core/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # This ensures Google/Social users get sent to /profile/their_username/
        return reverse('profile', kwargs={'username': request.user.username})

    def get_signup_redirect_url(self, request):
        # Same for new signups via social
        return reverse('profile', kwargs={'username': request.user.username})