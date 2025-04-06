from django import forms
from .models import Showcase

class ShowcaseForm(forms.ModelForm):
    class Meta:
        model = Showcase
        fields = ('title', 'description', 'industry', 'community')  # Exclude 'profile'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title for your showcase'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Describe your expertise or service'}),
            'industry': forms.Select(attrs={'placeholder': 'Select your industry'}),
            'community': forms.Select(attrs={'placeholder': 'Select a community (optional)'}),
        }