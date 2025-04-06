from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BetaTester

# Create your views here.

def index_view(request):
    return render(request, 'web/index.html')


def beta_signup_view(request):
    """Handles beta tester signups."""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        reason = request.POST.get('reason')

        # Save the beta tester information
        BetaTester.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            reason=reason
        )
        messages.success(request, 'Thank you for signing up! We will contact you soon.')
        return redirect('web:beta_landing')
    return render(request, 'web/beta.html')