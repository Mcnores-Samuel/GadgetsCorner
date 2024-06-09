#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module contains the AgentStockForm class, which is used to dynamically create
the AgentStock form to allow admin to add phones to their stock
"""
from django import forms
from ..models.agent_profile import AgentProfile


class AssignAgentForm(forms.Form):
    """Dynamically assigns lists all the agents and assigns them to a selected phone
    """
    choices = [(agent.user, agent.user) for agent in AgentProfile.objects.all()]
    agent = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
