from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class ZeedAccountAdapter(DefaultAccountAdapter):
    
    def get_login_redirect_url(self, request):
        """
        Routes users dynamically based on their onboarding status.
        """
        user = request.user
        
        # Check if the user has a profile or if they haven't finished onboarding
        # (Adjust 'has_selected_niche' to match whatever boolean or profile check you use)
        if hasattr(user, 'profile') and not user.profile.has_selected_niche:
            return reverse('niche_selection')
            
        # Returning users with finished profiles go to the feed or profile page
        return reverse('feed')

    def get_signup_redirect_url(self, request):
        """
        Where allauth maps new signups. Force them to niche selection.
        """
        return reverse('niche_selection')