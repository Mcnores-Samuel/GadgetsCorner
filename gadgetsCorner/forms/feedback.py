"""This module contains the forms related to the user profile."""
from django import forms
from ..models.feedback import Feedback


class FeedbackForm(forms.ModelForm):
    """Form for the feedback."""
    class Meta:
        """Meta class for the feedback form."""
        model = Feedback
        fields = ('feedback_type', 'feedback')
        widgets = {
            'feedback_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Feedback Type i.e. Bug Report, Feature Request, etc'}),
            'feedback': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Feedback Details'})
        }