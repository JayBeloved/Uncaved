from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required')
    email = forms.EmailField(max_length=254, required=True, help_text='Required')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class': 'form-control'})
            if 'password2' in self.fields:
                self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
            self.fields['password2'].label = "Confirm Password"
            self.fields['password2'].help_text = None
            self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
            self.fields['password1'].label = "Password"
            self.fields['password1'].help_text = None


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['country', 'headline', 'profile_image', 'bio',  'instagram', 'linkedin', 'website', 'twitter', 'facebook', 'youtube']
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'form-control form-select'}),
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'youtube': forms.TextInput(attrs={'class': 'form-control'}),
        }