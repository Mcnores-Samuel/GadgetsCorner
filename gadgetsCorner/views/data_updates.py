from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms.user_profile_update_form import UserProfileForm
from ..forms.users import UserAvatarForm
from ..models.main_storage import MainStorage
from django.http import JsonResponse
from ..models.user_profile import UserAvatar


@login_required
def profile(request):
    """Display the user's profile.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    profile_form = None
    if request.user.is_superuser:
        if request.method == 'POST':
            profile_form = UserProfileForm(request.POST, user=request.user)
            if profile_form.is_valid():
                profile = profile_form.process_profile()
                if profile:
                    messages.success(request, 'Your profile information was successfully updated.')
                    return redirect('profile')
                else:
                    messages.error(request, 'An error occurred while updating your profile information.')
                    return redirect('profile')
        else:
            profile_form = UserProfileForm(user=request.user)
        avatar = UserAvatar.objects.get(user=request.user) if UserAvatar.objects.filter(user=request.user).exists() else None
        context = {
                'profile': user.email[0],
                'user': user,
                'form': profile_form,
                'avatar': avatar
            }
        return render(request, 'users/admin_sites/profile.html', context)
    return redirect('dashboard')


@login_required
def upload_image(request):
    """Uploads the user's profile image.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        avatar_form = UserAvatarForm(request.POST, request.FILES)
        if avatar_form.is_valid():
            # Get or create UserAvatar instance for the current user
            avatar, created = UserAvatar.objects.get_or_create(user=request.user)
            
            if not created and avatar.image:
                avatar.image.delete()
            avatar.image = avatar_form.cleaned_data['image']
            avatar.save()
            messages.success(request, 'Your profile picture was successfully updated.')
            return redirect('profile')

    return redirect('profile')


@login_required
def change_password(request):
    """Change the user's password.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    if request.method == 'POST':
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(user)
    
    context = {
        'profile': user.email[0],
        'password_form': password_form,
    }
    return render(request, 'users/general-sites/change_password.html', context)


@login_required
def add_contract_number(request):
    """Adds contract number to the phone sold.
    user must be an agent to access this view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == 'POST':
        imei_number = request.POST.get('imei_number', None)
        contract_number = request.POST.get('contract_number', None)
        if contract_number and imei_number:
            main_storage = MainStorage.objects.get(device_imei=imei_number)
            if main_storage:
                main_storage.contract_no = contract_number
                main_storage.save()
                messages.success(request,
                                 'Contract No: {} for IMEI: {} added successfully'.format(
                                     contract_number, imei_number))
        if request.user.is_superuser:
            return redirect('pending_sales')
    return redirect('dashboard')
    
