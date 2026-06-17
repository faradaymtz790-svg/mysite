from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class ZeedAccountAdapter(DefaultAccountAdapter):
    
    def get_login_redirect_url(self, request):
        """
        Where users go right after logging in normally OR via social login.
        """
        # If they just signed up, redirect them to niche selection first
        if request.session.get('new_signup_redirect'):
            del request.session['new_signup_redirect']
            return reverse('niche_selection')
            
        # Returning users go straight to their profile
        return reverse('profile', kwargs={'username': request.user.username})

    def get_signup_redirect_url(self, request):
        """
        Where users go right after registering a brand-new account.
        """
        # Set the session flag just in case
        request.session['new_signup_redirect'] = True
        return reverse('niche_selection')