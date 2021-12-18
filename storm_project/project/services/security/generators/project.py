# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from elasticsearch_dsl import Q

from invenio_access import any_user
from flask_principal import UserNeed

from invenio_records.dictutils import dict_lookup

from invenio_records_permissions.generators import Generator


class BaseProjectGenerator(Generator):
    """Base generator for project records."""

    #
    # Access field (metadata) used to define the `needs`.
    #
    needs_access_field = None

    #
    # Access field (metadata) used to create query filters.
    #
    query_access_field = None

    def needs(self, record=None, **kwargs):
        """Needs to be a research project owner."""
        if record:
            record_owned_by_access = dict_lookup(record, self.needs_access_field) or []

            return [UserNeed(owner["user"]) for owner in record_owned_by_access]
        return [any_user]

    def query_filter(self, identity=None, **kwargs):
        """Only show record acessible for the current identity."""
        for need in identity.provides:
            if need.method == "id":
                return Q("term", **{self.query_access_field: identity.id})
        return []


class ResearchProjectOwner(BaseProjectGenerator):
    """Allows Research Project owners."""

    needs_access_field = "access.owned_by"
    query_access_field = "access.owned_by.user"


class ResearchProjectContributor(BaseProjectGenerator):
    """Allows Research Project contributors."""

    needs_access_field = "access.contributed_by"
    query_access_field = "access.contributed_by.user"
