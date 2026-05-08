from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'audio_comment']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Write your comment title...',
                'class': 'comment-input-style'
            }),
        }





from django import forms
# CHANGE THIS:
# from captcha.fields import ReCaptchaField

# TO THIS:
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

# --- Keep your existing functions/classes here ---
# class MyOldForm(forms.Form):
#     ...

# --- Add the new SignupForm below ---
class SignupForm(forms.Form):
    # Add your existing signup fields here, for example:
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    
    # This is the new security field
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)



from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'cover_photo', 'bio', 'location', 'links', 'niches']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'glass-input', 'rows': 3, 'maxlength': '500'}),
            'links': forms.URLInput(attrs={'class': 'glass-input', 'placeholder': 'https://...'}),
        }