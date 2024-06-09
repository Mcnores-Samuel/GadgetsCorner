#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the forms for easy search and filtering of the data."""
from django import forms


class FilterMainStoregeForm(forms.Form):
    search_query = forms.CharField(
        label='Search',
        max_length=100, required=False,
        widget=forms.TextInput(
            {"placeholder": "imei, model, date etc."}))
