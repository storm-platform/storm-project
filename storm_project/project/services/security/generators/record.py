# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request
from flask_principal import UserNeed

from elasticsearch_dsl import Q

from storm_project.proxies import current_project
from invenio_records_permissions.generators import Generator


class ProjectRecordQueryFilterGenerator(Generator):
    """Base filter records generator.

    This base generator filters the records based on the user' permissions in
    the project in which the record is registered.
    """

    query_use_parent_access_definitions = True
    """Define if the access is based on the record itself or record parent."""

    def __init__(self, use_parent_access=True):
        self.query_use_parent_access_definitions = use_parent_access

    def query_filter(self, identity=None, **kwargs):
        """Only show record accessible for the current identity."""

        # special case: We need to check for the project context also.
        # So, for this filter, we will include the project_id to search
        # the `owned_by` since the records only have `project` as
        # owners.
        project_id = request.view_args.get("project_id")

        # maybe users are not available. But, even for this case,
        # we need to check the project context.
        users = [n.value for n in identity.provides if n.method == "id"] or []

        # some records don't have an associated parent.
        parent_string = ""
        if self.query_use_parent_access_definitions:
            parent_string = "parent."

        return Q("terms", **{f"{parent_string}access.contributed_by.user": users}) & Q(
            "terms", **{f"{parent_string}access.owned_by.project": [project_id]}
        )


class ProjectRecordAgent(ProjectRecordQueryFilterGenerator):
    """Generator to define users that colaborate with the project records.

    This generator defines a generic way to check if the users have permissions
    to access a given project and their records. This generator must be subclassed
    to be used. All subclasses must implement the method ``_select_record_agent``.
    """

    def _select_record_agent(self, record, **kwargs):
        """Method that allows users to define the rules used to
        extract the project ``owners`` and ``colaborators`` from a record.

        This method must return a tuple with (``owners``, ``contributors``), where
        `owners` and `contributors` are list of ``storm_commons.systemfields.models.Agent``.
        """
        raise NotImplemented(
            "It's necessary define the rule used to select the owners and colaborators"
        )

    def needs(self, record=None, **kwargs):
        """Needs to be a project user with access to the selected record."""
        if record:
            # selecting the records to apply the access verification rules.
            owners, contributors = self._select_record_agent(record, **kwargs)

            # Filter the owners by the accessed project.
            project_id = request.view_args.get("project_id")

            if project_id not in [o._entity.data.get("id") for o in owners]:
                return []  # invalid project!

            else:
                # if valid, create the UserNeed based on the users
                # available in the project.
                needs = []

                # is assumed that ``owner` is a ``project``.
                for owner_agent in owners:
                    if owner_agent.agent_type == "project":

                        # extracting the data
                        owner_agent_access = owner_agent._entity.data.get("access")

                        agent_owners = owner_agent_access.get("owned_by")
                        agent_contributors = owner_agent_access.get("contributed_by")

                        # creating the needs.
                        users_agents = [
                            *agent_owners,
                            *agent_contributors,
                        ]

                        # is assumed that, all ``owner_agents`` are agent ``user``.
                        users = [p["user"] for p in users_agents]

                        needs.extend(
                            u.agent_id for u in contributors if u.agent_id in set(users)
                        )

                return [UserNeed(u) for u in set(needs)]
        return []


class ProjectRecordUser(ProjectRecordQueryFilterGenerator):
    """Generator to define if user has access to
    the selected project."""

    only_owners = False
    """Flag to enable only project owners as valid project users (Default is false)."""

    def __init__(self, use_parent_access=True, only_owners=False):
        self.only_owners = only_owners
        super(ProjectRecordUser, self).__init__(use_parent_access)

    def needs(self, record=None, **kwargs):
        """Needs to define if the user has access to the selected project."""

        # extracting the data
        project_owners = current_project._obj.access.owners
        project_contributors = current_project._obj.access.contributors

        project_users = project_owners
        if not self.only_owners:
            project_users = [*project_users, *project_contributors]

        # select only the users.
        valid_project_ids = [
            obj.agent_id for obj in project_users if obj.agent_type == "user"
        ]

        return [UserNeed(uid) for uid in set(valid_project_ids)]
