#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the SignUpForm class,
which is used to dynamically create
the user sign up form to allow users to
sign up to access user privillegies
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models.user_profile import UserProfile


class SignUpForm(UserCreationForm):
    """Dynamically create the user sign in form to allow users to sign in
    to access user privillegies
    """
    agent_code = forms.CharField(max_length=100, required=False)

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password1',
                  'password2', 'agent_code')

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['agent_code']
        for field_name in required_fields:
            field_value = cleaned_data.get(field_name)
            if not field_value:
                self.add_error(field_name, 'Agent code is required for agent registration')

        return cleaned_data
