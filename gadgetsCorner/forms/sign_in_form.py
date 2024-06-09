#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the SignInForm class,
which is used to dynamically create the user
sign in form to allow users to sign in to access user privillegies
"""
from django import forms


class SignInForm(forms.Form):
    """The SignInForm class is responsible for handling the sign in form.

    This form is used in the sign in page to facilitate the sign in process.
    It validates the user's email and password and ensures that the user is
    a staff member.

    Form Fields:
        - email: Email of the user.
        - password: Password of the user.
        - remember_me: Boolean field indicating whether the user wants to stay
            signed in.
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    remember_me = forms.BooleanField(
        required=False, initial=True,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}))
