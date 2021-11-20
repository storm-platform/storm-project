# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask_principal import UserNeed

from elasticsearch_dsl import Q
from invenio_access import any_user

from invenio_records_permissions.generators import (
    AuthenticatedUser,
    Generator,
    SystemProcess,
)
from invenio_records_permissions.policies import BasePermissionPolicy

from invenio_records.dictutils import dict_lookup


class ResearchProjectOwners(Generator):
    """Allows Research Project owners."""

    def needs(self, record=None, **kwargs):
        """Needs to research project owners."""
        if record:
            record_owned_by_access = dict_lookup(record, "access.owned_by") or []

            return [UserNeed(owner["user"]) for owner in record_owned_by_access]
        return [any_user]

    def query_filter(self, identity=None, **kwargs):
        """Only show record acessible for the current identity."""
        for need in identity.provides:
            if need.method == "id":
                return Q("term", **{"access.owned_by.user": identity.id})
        return []


class ResearchProjectContributors(Generator):
    """Allows Research Project contributors."""

    def needs(self, record=None, **kwargs):
        """Needs to research project contributors."""
        if record:
            record_contributors = dict_lookup(record, "access.contributed_by") or []

            return [
                UserNeed(contributor["user"]) for contributor in record_contributors
            ]
        return [any_user]

    def query_filter(self, identity=None, **kwargs):
        """Only show record acessible for the current identity."""
        for need in identity.provides:
            if need.method == "id":
                return Q("term", **{"access.contributed_by.user": identity.id})
        return []


class ResearchProjectPermissionPolicy(BasePermissionPolicy):

    #
    # High level permissions
    #
    can_use = [ResearchProjectOwners(), ResearchProjectContributors(), SystemProcess()]

    can_manage = [ResearchProjectOwners(), SystemProcess()]

    #
    # Low level permissions
    #
    can_create = [AuthenticatedUser(), SystemProcess()]

    can_read = can_use

    can_update = can_manage

    can_delete = can_manage

    can_search = can_use

    can_search_user_project_research = can_use
