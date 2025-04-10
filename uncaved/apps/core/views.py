from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Showcase, Community
from uncaved.apps.accounts.models import Profile
from .forms import ShowcaseForm
from django_countries import countries
from django.contrib.auth.models import User

# Options for Industry Choices
INDUSTRY_CHOICES = [
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
]

@login_required
def dashboard_view(request):
    """Dashboard view for signed-in users."""
    user = request.user
    logged_profile = Profile.objects.filter(user=user).first()
    profile = user.profile  # Access the user's profile
    showcase = Showcase.objects.filter(profile=logged_profile).first()  # Get the user's first showcase, if any
    total_users = User.objects.count()
    same_country_users = User.objects.filter(profile__country=profile.country).count()
    same_industry_users = Showcase.objects.filter(industry=showcase.industry).count() if showcase else 0
    total_communities = Community.objects.count()
    user_communities = Community.objects.filter(members=profile).count()

    context = {
        'user': user,
        'profile': profile,
        'showcase': showcase,
        'total_users': total_users,
        'same_country_users': same_country_users,
        'same_industry_users': same_industry_users,
        'total_communities': total_communities,
        'user_communities': user_communities,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def create_showcase_view(request):
    """View to create a new showcase."""
    if request.method == 'POST':
        form = ShowcaseForm(request.POST)
        if form.is_valid():
            showcase = form.save(commit=False)
            showcase.profile = request.user.profile  # Set the profile to the logged-in user's profile
            showcase.save()
            return redirect('core:showcase_detail', showcase_id=showcase.id)
    else:
        form = ShowcaseForm()
    return render(request, 'core/create_showcase.html', {'form': form})


@login_required
def edit_showcase_view(request, showcase_id):
    """View to edit an existing showcase."""
    showcase = get_object_or_404(Showcase, id=showcase_id, profile=request.user.profile)  # Ensure the user owns the showcase
    if request.method == 'POST':
        form = ShowcaseForm(request.POST, instance=showcase)
        if form.is_valid():
            form.save()
            return redirect('core:showcase_detail', showcase_id=showcase.id)
    else:
        form = ShowcaseForm(instance=showcase)
    return render(request, 'core/edit_showcase.html', {'form': form})


def showcase_detail_view(request, showcase_id):
    """View to display the details of a showcase."""
    showcase = get_object_or_404(Showcase, id=showcase_id)
    showcase.clicks += 1
    showcase.save()

    # Fetch similar showcases based on industry or community
    similar_showcases = Showcase.objects.filter(
        Q(industry=showcase.industry) | Q(community=showcase.community)
    ).exclude(id=showcase.id)[:5]  # Exclude the current showcase and limit to 5

    context = {
        'showcase': showcase,
        'similar_showcases': similar_showcases,
    }
    return render(request, 'core/showcase_detail.html', context)


def showcase_board_view(request):
    """View to display all showcases in a board layout."""
    country_choices = countries
    industry_choices = INDUSTRY_CHOICES
    showcases = Showcase.objects.all()
    top_showcases = showcases.order_by('-likes')[:5]

    # Filter by industry, country, or keywords
    industry = request.GET.get('industry')
    country = request.GET.get('country')
    keywords = request.GET.get('keywords')

    if industry:
        showcases = showcases.filter(industry=industry)
    if country:
        showcases = showcases.filter(user__profile__country=country)
    if keywords:
        showcases = showcases.filter(
            Q(title__icontains=keywords) | Q(description__icontains=keywords)
        )

    # Paginate the showcases
    paginator = Paginator(showcases, 12)  # Show 12 showcases per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'country_choices': country_choices,
        'industry_choices': industry_choices,
        'top_showcases': top_showcases,
        'industry': industry,
        'country': country,
        'keywords': keywords,
    }
    return render(request, 'core/showcase_board.html', context)


def like_showcase(request, showcase_id):
    """View to like or unlike a showcase."""
    showcase = get_object_or_404(Showcase, id=showcase_id)
    if request.user in showcase.likes.all():
        showcase.likes.remove(request.user)
        liked = False
    else:
        showcase.likes.add(request.user)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': showcase.likes.count()})

@login_required
def my_showcases_view(request):
    """View to display the logged-in user's showcases."""
    user = request.user
    profile = user.profile  # Access the user's profile
    showcases = Showcase.objects.filter(profile=profile)  # Get the user's showcases
    context = {
        'user': user,
        'profile': profile,
        'showcases': showcases,
    }
    return render(request, 'core/my_showcases.html', context)


def community_list_view(request):
    """View to display all communities."""
    communities = Community.objects.all()
    context = {
        'communities': communities,
    }
    return render(request, 'core/community_list.html', context)

def community_detail_view(request, community_id):
    """View to display the details of a community."""
    community = get_object_or_404(Community, id=community_id)
    context = {
        'community': community,
    }
    return render(request, 'core/community_detail.html', context)

def join_community_view(request, community_id):
    """View to join a community."""
    community = get_object_or_404(Community, id=community_id)
    profile = request.user.profile  # Access the user's profile
    if request.method == 'POST':
        if profile not in community.members.all():
            community.members.add(profile)
            community.save()
            return redirect('core:community_detail', community_id=community.id)
    return render(request, 'core/join_community.html', {'community': community})


@login_required
def create_community_view(request):
    """View to create a new community."""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_public = request.POST.get('is_public') == 'on'
        community = Community.objects.create(
            name=name,
            description=description,
            created_by=request.user,
            is_public=is_public
        )
        community.members.add(request.user.profile)  # Add the creator to the community
        return redirect('core:community_detail', community_id=community.id)
    return render(request, 'core/create_community.html')

@login_required
def my_communities_view(request):
    """View to display the communities the user has joined."""
    profile = request.user.profile
    communities = Community.objects.filter(members=profile)
    context = {
        'communities': communities,
    }
    return render(request, 'core/my_communities.html', context)
