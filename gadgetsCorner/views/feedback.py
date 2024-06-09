"""This module contains the views related to the feedback."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms.feedback import FeedbackForm
from ..models.feedback import Feedback
from django.utils import timezone


@login_required
def feedback(request):
    """Display the feedback form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.user.is_superuser:
        if request.method == 'POST':
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user
                feedback.date = timezone.now()
                feedback.save()
                messages.success(request, 'Your feedback was successfully submitted.')
                return redirect('feedback')
            else:
                messages.error(request, 'An error occurred while submitting your feedback.')
                return redirect('feedback')
        else:
            feedback_form = FeedbackForm()
        return render(request, 'users/admin_sites/feedback.html', {'form': feedback_form})
    return redirect('dashboard')