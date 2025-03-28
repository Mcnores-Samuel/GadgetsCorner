

from ...forms.sign_up_form import SignUpForm
from ...forms.sign_in_form import SignInForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django_email_verification import send_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages



def sign_up(request):
    """
    The `sign_up` view function handles user registration and sign-up processes.

    Functionality:
    - Allows users to create new accounts by providing necessary registration details.
    - Validates user input, ensuring it meets specified criteria.
    - Upon successful registration, creates a new user account and redirects to the
      sign-in page.

    Parameters:
    - request: The HTTP request object containing user registration data.

    Returns:
    - Renders the registration form for users to input their registration details.
    - Redirects to the sign-in page after successful registration.

    Usage:
    - Users access this view to create new accounts within the application.
    - Ensures a seamless registration process while maintaining data integrity.

    Note:
    - User authentication and validation logic should be implemented in the associated
      authentication system.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email(user)
            return render(request, 'authentication/confirm_email.html', {'user': user})
        else:
            messages.error(request, "Invalid agent code, please contact your admin for a valid agent code.")
        for field in form:
            for error in field.errors:
                messages.error(request, f"{error}")
    else:
        form = SignUpForm()
    return render(request, 'authentication/sign_up.html', {'form': form})


def sign_in(request):
    """
    The `sign_in` view function handles user authentication and sign-in processes.

    Functionality:
    - Allows registered users to sign in by providing their credentials (e.g., email
      and password).
    - Validates user credentials and, upon success, grants access to the application.
    - Displays appropriate error messages in case of unsuccessful sign-in attempts.

    Parameters:
    - request: The HTTP request object containing user authentication data.

    Returns:
    - Renders the sign-in form for users to input their credentials.
    - Grants access to the application dashboard upon successful sign-in.
    - Displays error messages for invalid sign-in attempts.

    Usage:
    - Registered users access this view to log in and access the application's features.
    - Includes user authentication and session management logic.

    Note:
    - User authentication and validation should be handled by the authentication system.
    """
    user = None
    if request.method == "POST":
        try:
            form = SignInForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                remember_me = form.cleaned_data['remember_me']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if remember_me:
                            request.session.set_expiry(604800)
                        else:
                            request.session.set_expiry(604800)
                        if user.is_staff:
                            if user.last_login:
                                messages.success(request, 'Welcome back, {}'.format(user.username))
                            else:
                                messages.success(request, 'Welcome, {}'.format(user.username))
                            return redirect(reverse('dashboard'))
                    else:
                        form.add_error(None, "Please!! activate your account")
                else:
                    form.add_error(None, "Invalid username or password")
        except Exception:
            form = SignInForm()
            messages.error(request, 'Something went wrong, please try again')
            return render(request, 'authentication/sign_in.html', {'form': form, 'user': user})
    else:
        form = SignInForm()
    return render(request, 'authentication/sign_in.html', {'form': form, 'user': user})


@login_required
def resend_confirmation_email(request):
    user = request.user
    if not user.is_active:
        send_email(user)
    return render(request, 'authentication/confirm_email.html')


@login_required
def sign_out(request):
    """The `sign_out` view function is responsible for handling user sign-out.
    """
    logout(request)
    return redirect(reverse('home_page'))
