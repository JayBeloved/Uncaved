# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm, SignUpForm, ProfileForm, ProfileImageForm
from .models import Profile


# def home_view(request):
#     return HttpResponseRedirect(reverse('accounts:login'))

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("core:dashboard")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/sign-in.html", {"form": form, "msg": msg})

def logout_view(request):
    logout(request)
    return redirect('web:index')


def sign_up(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create an empty profile for the user
            Profile.objects.create(user=user)
            messages.success(request, 'Account created successfully. Please log in to complete your profile.')
            return redirect('accounts:signin')
        else:
            messages.error(request, 'There was an error creating your account.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/sign-up.html', {'form': form})


@login_required
def view_profile(request):
    """Displays the user's profile."""
    profile = request.user.profile
    return render(request, 'accounts/view_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Allows the user to edit their profile."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Preserve the current profile image if no new image is uploaded
            if not request.FILES.get('profile_image'):
                form.instance.profile_image = profile.profile_image
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:view_profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def update_profile_image(request):
    """Allows the user to update their profile picture."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile picture has been updated successfully.')
            return redirect('accounts:view_profile')
    else:
        form = ProfileImageForm(instance=profile)
    return render(request, 'accounts/update_profile_image.html', {'form': form})
