#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""This module contains the forms related to the user profile."""
from django import forms
from ..models.user_profile import UserAvatar


class UserAvatarForm(forms.ModelForm):
    """Form for the user avatar."""
    class Meta:
        """Meta class for the user avatar form."""
        model = UserAvatar
        fields = ('image',)
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'})
        }