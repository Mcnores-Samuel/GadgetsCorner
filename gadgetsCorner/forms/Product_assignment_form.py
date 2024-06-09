#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the forms for the data entry."""
from django import forms


PHONELIST = (
        ("S18", "S18"), ("A60", "A60"),
        ("A04", "A04"), ("A18", "A18"),
        ("C20", "C20"), ("C19", "C19"),
        ("S10", "S10"), ("10C8G", "10C8G"),
        ("10C", "10C"), ("8C", "8C"),
        ("P7P4G", "P7P4G"), ("P7P3G", "P7P3G"),
        ("P7", "P7"), ("S9", "S9"), ('9T', '9T'),
        ("S8", "S8"), ("S7", "S7"),
    )


class ProductAssignmentForm(forms.Form):
    phone_type = forms.ChoiceField(
        label='Phone type', required=True,
        choices=PHONELIST)
    image = forms.ImageField(label='Image', required=False)
