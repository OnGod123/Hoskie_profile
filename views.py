from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def handle_user_profiles(request, profile_id):
    user_profile = get_object_or_404(UserProfile, pk=profile_id)

    if request.method == 'POST' and request.user == user_profile.user:
        # Only allow the owner of the profile to update the profile picture
        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.save()
            return redirect('user_profile', profile_id=profile_id)

    # Retrieve all user profiles to display (for viewing purposes)
    all_user_profiles = UserProfile.objects.filter(user=request.user)

    context = {
        'user_profile': user_profile,
        'all_user_profiles': all_user_profiles,
    }
    return render(request, 'user_profile.html', context)

