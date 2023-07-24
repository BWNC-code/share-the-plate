from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please use a valid email address.')
    bio = forms.CharField(required=False, help_text='Optional. A short description about you.')
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload a profile picture.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                bio=self.cleaned_data['bio'],
                profile_picture=self.cleaned_data.get('profile_picture', 'default_profile.jpg')
            )
        return user
