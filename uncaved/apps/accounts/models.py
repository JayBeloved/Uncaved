from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
import os
import logging

logger = logging.getLogger(__name__)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)', default='NG')
    headline = models.CharField(max_length=150, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    youtube = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        logger.info(f"Saving profile for user: {self.user.username}")
        try:
            if self.profile_image:
                # Get the file extension
                ext = os.path.splitext(self.profile_image.name)[1]
                # Rename the file to the user's username
                new_filename = f"{self.user.username}{ext}"
                # Save the file with the new name - include the folder!
                self.profile_image.name = f"profile_pics/{new_filename}"

                print(f"Saving file to: {self.profile_image.name}")

            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving profile image: {e}")
            raise

    def __str__(self):
        return f"{self.user.username}'s Profile"
