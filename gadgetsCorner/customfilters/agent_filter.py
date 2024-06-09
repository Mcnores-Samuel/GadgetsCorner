"""This module contains the agent filter for the main storage model."""

from django.utils.translation import gettext_lazy as _
from django.contrib import admin


class AgentFilter(admin.SimpleListFilter):
    """This class contains the agent filter for the main storage model.

    Attributes:
      title (str): The title of the filter.
      parameter_name (str): The parameter name of the filter.
    """
    title = _('Sales Agents')
    parameter_name = 'agent'

    def lookups(self, request, model_admin):
        """Return a list of tuples.

        Returns:
          list: A list of tuples containing the agent IDs and usernames.
        """
        agents = model_admin.model.objects.filter(agent__groups__name='agents') \
                                            .values_list('agent__username', flat=True) \
                                            .distinct()
        return [(agent, agent) for agent in agents]
    
    def queryset(self, request, queryset):
        """Return the filtered queryset.

        Args:
          request (HttpRequest): The HTTP request object.
          queryset (QuerySet): The queryset to filter.

        Returns:
          QuerySet: The filtered queryset.
        """
        if self.value():
            return queryset.filter(agent__username=self.value())
        return queryset
    

class SpecialAgentsFilter(admin.SimpleListFilter):
    """This class contains the special agents filter for the main storage model.

    Attributes:
      title (str): The title of the filter.
      parameter_name (str): The parameter name of the filter.
    """
    title = _('Special Agents')
    parameter_name = 'agent'

    def lookups(self, request, model_admin):
        """Return a list of tuples.

        Returns:
          list: A list of tuples containing the agent IDs and usernames.
        """
        agents = model_admin.model.objects.filter(agent__groups__name='special_sales') \
                                            .values_list('agent__username', flat=True) \
                                            .distinct()
        return [(agent, agent) for agent in agents]
    
    def queryset(self, request, queryset):
        """Return the filtered queryset.

        Args:
          request (HttpRequest): The HTTP request object.
          queryset (QuerySet): The queryset to filter.

        Returns:
          QuerySet: The filtered queryset.
        """
        if self.value():
            return queryset.filter(agent__username=self.value())
        return queryset
    

class AirtelAgentFilter(admin.SimpleListFilter):
    """This class contains the airtel agent filter for the main storage model.

    Attributes:
      title (str): The title of the filter.
      parameter_name (str): The parameter name of the filter.
    """
    title = _('Airtel Agents')
    parameter_name = 'agent'

    def lookups(self, request, model_admin):
        """Return a list of tuples.

        Returns:
          list: A list of tuples containing the agent IDs and usernames.
        """
        agents = model_admin.model.objects.filter(agent__groups__name='airtel_agents') \
                                            .values_list('agent__username', flat=True) \
                                            .distinct()
        print(agents)
        return [(agent, agent) for agent in agents]
    
    def queryset(self, request, queryset):
        """Return the filtered queryset.

        Args:
          request (HttpRequest): The HTTP request object.
          queryset (QuerySet): The queryset to filter.

        Returns:
          QuerySet: The filtered queryset.
        """
        if self.value():
            return queryset.filter(agent__username=self.value())
        return queryset