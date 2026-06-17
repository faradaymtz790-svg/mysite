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

# --- Keep your existing functions/classes here ---
# class MyOldForm(forms.Form):
#     ...

# --- Updated SignupForm ---
class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'placeholder': 'Pick a unique username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'name@example.com'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'id': 'phone'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password', 'placeholder': 'Create a password'})
    )
    confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'confirm', 'placeholder': 'Repeat your password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")

        # Basic backend alignment check for passwords matching
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords do not match.")
            
        return cleaned_data





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





        # forms.py
