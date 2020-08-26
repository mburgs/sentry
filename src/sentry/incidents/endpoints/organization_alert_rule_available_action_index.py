from __future__ import absolute_import

from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response

from sentry import features
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.incidents.endpoints.bases import OrganizationEndpoint
from sentry.incidents.endpoints.serializers import action_target_type_to_string
from sentry.incidents.logic import (
    get_available_action_integrations_for_org,
    get_pagerduty_services,
)
from sentry.incidents.models import AlertRuleTriggerAction


def build_action_response(registered_type, integration=None, organization=None):
    """
    Build the "available action" objects for the API. Each one can have different fields.

    :param registered_type: One of the registered AlertRuleTriggerAction types.
    :param integration: Optional. The Integration if this action uses a one.
    :param organization: Optional. If this is a PagerDuty action, we need the organization to look up services.
    :return: The available action object.
    """

    action_response = {
        "type": registered_type.slug,
        "allowedTargetTypes": [
            action_target_type_to_string.get(target_type)
            for target_type in registered_type.supported_target_types
        ],
    }

    if integration:
        action_response["integrationName"] = integration.name
        action_response["integrationId"] = integration.id

        if registered_type.type == AlertRuleTriggerAction.Type.PAGERDUTY:
            action_response["options"] = [
                {"value": service["id"], "label": service["service_name"]}
                for service in get_pagerduty_services(organization, integration.id)
            ]

    return action_response


class OrganizationAlertRuleAvailableActionIndexEndpoint(OrganizationEndpoint):
    def get(self, request, organization):
        """
        Fetches actions that an alert rule can perform for an organization
        """
        if not features.has("organizations:incidents", organization, actor=request.user):
            raise ResourceDoesNotExist

        actions = []

        # Cache Integration objects in this data structure to save DB calls.
        provider_integrations = defaultdict(list)
        for integration in get_available_action_integrations_for_org(organization):
            provider_integrations[integration.provider].append(integration)

        for registered_type in AlertRuleTriggerAction.get_registered_types():
            # Used cached integrations for each `registered_type` instead of making N calls.
            if registered_type.integration_provider:
                actions += [
                    build_action_response(
                        registered_type, integration=integration, organization=organization
                    )
                    for integration in provider_integrations[registered_type.integration_provider]
                ]

            else:
                actions.append(build_action_response(registered_type))
        return Response(actions, status=status.HTTP_200_OK)
