#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the filters for easy
search and filtering of the data.
"""
import django_filters
from ..models.main_storage import MainStorage
from ..models.user_profile import UserProfile
from django import forms
from django.utils import timezone


class FilterMainStorege(django_filters.FilterSet):
    """Filter for the main storage."""
    class Meta:
        model = MainStorage
        fields = ('in_stock', 'assigned', 'phone_type',)


class FilterAgentAndData(forms.Form):
    """Filter for the agent and data."""

    user = forms.ModelChoiceField(
        queryset=UserProfile.objects.all().order_by('id'),
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose agent',
                'required': 'required',
            }
        )
    )


class FilterAgentAndDataSales(forms.Form):

    """Filter for the agent and data."""

    month = forms.ChoiceField(
        choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
                 ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'),
                 ('10', 'October'), ('11', 'November'), ('12', 'December')],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose month',
                'required': 'required',
            }
        )
    )
    
    year = forms.ChoiceField(
        choices=[(timezone.now().date().year, timezone.now().date().year),
                 (timezone.now().date().year - 1, timezone.now().date().year - 1),
                 (timezone.now().date().year - 2, timezone.now().date().year - 2),
                 (timezone.now().date().year - 3, timezone.now().date().year - 3),
                 (timezone.now().date().year - 4, timezone.now().date().year - 4)],
        widget=forms.Select(
            attrs={
                'class': 'form-control W-25',
                'placeholder': 'Choose year',
                'required': 'required',
            }
        )
    )
