from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Recipe, Category


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             help_text='A valid email addres is required'
                             )
    bio = forms.CharField(required=False,
                          help_text='Optional. A short description about you.')
    profile_picture = forms.ImageField(required=False,
                                       help_text='Optional. Upload a profile picture.')

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
                profile_picture=self.cleaned_data.get('profile_picture',
                                                      'default_profile.jpg')
            )
        return user


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
                                                queryset=Category.objects.all(),
                                                )
    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags.",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = Recipe
        fields = ['title',
                  'ingredients',
                  'instructions',
                  'cooking_time',
                  'difficulty_level',
                  'featured_image',
                  'categories'
                  ]