#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the UserProfileForm class, which is used to dynamically create
the user profile form to allow users to update their profile information
"""
from django import forms
from ..models.contacts import Contact


class UserProfileForm(forms.Form):
    """The `UserProfileForm` class is responsible for handling the update of a user's
    profile information.
    """
    name = forms.CharField(
        label='Name',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        label='Email',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Phone Number',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Address',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        label='City',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    state = forms.CharField(
        label='State',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    zip_code = forms.CharField(
        label='Zip Code',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    current_location = forms.CharField(
        label='Current Location',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        """Override the default `__init__` method to dynamically add fields to the form
        based on the user's profile information.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            try:
                contact = Contact.objects.get(user=self.user)
                self.fields['name'].initial = contact.name
                self.fields['email'].initial = contact.email
                self.fields['phone'].initial = contact.phone
                self.fields['address'].initial = contact.address
                self.fields['city'].initial = contact.city
                self.fields['state'].initial = contact.state
                self.fields['zip_code'].initial = contact.zip_code
                self.fields['current_location'].initial = contact.current_location
            except Contact.DoesNotExist:
                pass
        
    def process_profile(self):
        """Process the profile information."""
        if self.user:
            try:
                contact = Contact.objects.get(user=self.user)
                contact.name = self.cleaned_data.get('name')
                contact.email = self.cleaned_data.get('email')
                contact.phone = self.cleaned_data.get('phone')
                contact.address = self.cleaned_data.get('address')
                contact.city = self.cleaned_data.get('city')
                contact.state = self.cleaned_data.get('state')
                contact.zip_code = self.cleaned_data.get('zip_code')
                contact.current_location = self.cleaned_data.get('current_location')
                contact.save()
            except Contact.DoesNotExist:
                Contact.objects.create(
                    user=self.user,
                    name=self.cleaned_data.get('name'),
                    email=self.cleaned_data.get('email'),
                    phone=self.cleaned_data.get('phone'),
                    address=self.cleaned_data.get('address'),
                    city=self.cleaned_data.get('city'),
                    state=self.cleaned_data.get('state'),
                    zip_code=self.cleaned_data.get('zip_code'),
                    current_location=self.cleaned_data.get('current_location')
                )
            return True
        return False