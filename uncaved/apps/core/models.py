from django.db import models
from django.contrib.auth.models import User
from uncaved.apps.accounts.models import Profile  # Import the Profile model from the accounts app

class Showcase(models.Model):
    """Represents individual user entries (formerly pitches) within a community or globally."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="showcases")  # Link to Profile
    community = models.ForeignKey('Community', on_delete=models.SET_NULL, null=True, blank=True, related_name="showcases")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=7000)
    industry = models.CharField(
        max_length=100,
        choices=[
            ('tech', 'Technology'),
            ('finance', 'Finance'),
            ('health', 'Healthcare'),
            ('education', 'Education'),
            ('entertainment', 'Entertainment'),
            ('retail', 'Retail'),
            ('manufacturing', 'Manufacturing'),
            ('real_estate', 'Real Estate'),
            ('transportation', 'Transportation'),
            ('energy', 'Energy'),
            ('agriculture', 'Agriculture'),
            ('hospitality', 'Hospitality'),
            ('construction', 'Construction'),
            ('legal', 'Legal'),
            ('marketing', 'Marketing'),
            ('media', 'Media'),
            ('non_profit', 'Non-Profit'),
            ('sports', 'Sports'),
            ('telecommunications', 'Telecommunications'),
            ('utilities', 'Utilities'),
            ('other', 'Other'),
        ],
        blank=True,
    )
    likes = models.ManyToManyField(User, related_name="liked_showcases", blank=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.profile.user.username}"
    
    
class Community(models.Model):
    """Represents a community where users can join and showcase their expertise."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_communities")
    members = models.ManyToManyField(Profile, related_name="joined_communities", blank=True)  # Link to Profile
    is_public = models.BooleanField(default=True)  # Public or private community
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name