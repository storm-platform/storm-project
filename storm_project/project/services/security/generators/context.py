# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request
from flask_principal import UserNeed

from elasticsearch_dsl import Q

from storm_project import current_project

from invenio_access import authenticated_user
from invenio_records_permissions.generators import Generator


class BaseStoredProjectContextGenerator(Generator):
    """Generator to define a user as colaborator based on
    the records information (Record without access field and index)."""

    # Project API class used to access
    # and handle the project informations.
    project_api_cls = None

    def needs(self, record=None, **kwargs):
        """Needs to be a project user with access to the selected record."""
        if record:
            # creating the research project (api) to smooth
            # the data selection.
            research_project = self.project_api_cls(
                data=record.project.data, model=record.project
            )

            # project context: this generator use the project
            # as basis to define the ``needs``
            owners = research_project.access.owners
            contributors = research_project.access.contributors

            people = set([o.agent_id for o in [*owners, *contributors]])

            # checking the context (flask.request is temporary)
            project_id = request.view_args.get("project_id")
            if project_id != research_project.pid.pid_value:
                return []

            # creating the needs only for project users
            return [UserNeed(i) for i in {record.user_id}.intersection(people)]

        # temporary: in the future, we can improve
        # this verifications using roles.
        return UserInProject().needs(record)


class BaseIndexedProjectContextGenerator(Generator):
    """Base generator to use the project context in the record permissions."""

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

        return Q("terms", **{"parent.access.contributed_by.user": users}) & Q(
            "terms", **{"parent.access.owned_by.project": [project_id]}
        )


class UserInProject(BaseIndexedProjectContextGenerator):
    """Generator to define if user has access to
    the selected project."""

    def needs(self, record=None, **kwargs):
        """Needs to define if the user has access to the selected project."""

        # we only check for a project context when the record is None, because
        # is assumed that record == None is a ``create`` operation.
        if record is None:
            # extracting the data
            project_owners = current_project._obj.access.owners
            project_contributors = current_project._obj.access.contributors

            # select only the users.
            valid_project_ids = [
                obj.agent_id
                for obj in [*project_owners, *project_contributors]
                if obj.agent_type == "user"
            ]

            return [UserNeed(uid) for uid in set(valid_project_ids)]
        return []


class BaseRecordColaboratorGenerator(BaseIndexedProjectContextGenerator):
    """Generic generator to define a user, inside the project,
    with access to the records.

    Note: The ``Colaborator`` in the class name, references both ``Owner`` and ``Contributor``.
    """

    def _select_record_rule(self, record, **kwargs):
        """Method that allows users to define the rules used to
        extract the `owners` and `colaborators` from a record.

        This method must be return a tuple with (`owners`, `contributors`), where
        `owners` and `contributors` are list of `storm_commons.systemfields.models.Agent`.
        """
        raise NotImplemented(
            "It's necessary define the rule used to select the owners and colaborators"
        )

    def needs(self, record=None, **kwargs):
        """Needs to be a project user with access to the selected record."""
        if record:
            # selecting the records to apply the access verification rules.
            parent_owners, parent_contributors = self._select_record_rule(
                record, **kwargs
            )

            # Filter the owners by the accessed project.
            project_id = request.view_args.get("project_id")

            if project_id not in [o._entity.data.get("id") for o in parent_owners]:
                return []  # invalid project!

            else:
                # if valid, create the UserNeed based on the users
                # available in the project.
                needs = []

                # is assumed that owner is a `project`.
                for parent_owner in parent_owners:
                    if parent_owner.agent_type == "project":
                        # extracting the data
                        parent_owner_access = parent_owner._entity.data.get("access")
                        parent_owner_owners = parent_owner_access.get("owned_by")
                        parent_owner_contributors = parent_owner_access.get(
                            "contributed_by"
                        )

                        # creating the needs.
                        parent_owner_people = [
                            *parent_owner_owners,
                            *parent_owner_contributors,
                        ]
                        parent_owner_people = [p["user"] for p in parent_owner_people]

                        needs.extend(
                            u.agent_id
                            for u in parent_contributors
                            if u.agent_id in set(parent_owner_people)
                        )

                return [UserNeed(u) for u in set(needs)]
        # From invenio-rdm-records:
        # 'record is None' means that this must be a 'create'
        # this should be allowed for any authenticated user
        return [authenticated_user]


class ProjectRecordColaborator(BaseRecordColaboratorGenerator):
    """Generator to define a user colaborator based on the
    record informations (without parent)."""

    def _select_record_rule(self, record, **kwargs):
        # note: Is assumed that the attribute `access` is a `RecordAccessField`.
        return record.access.owners, record.access.contributors


class VersionedProjectRecordColaborator(BaseRecordColaboratorGenerator):
    """Generator to define a user colaborator based on the record parent (versioned)
    informations."""

    def _select_record_rule(self, record, **kwargs):
        # checking if the user is a `contributor` or `owner` of the requested record.
        # note: Is assumed that the `parent` attribute use the `RecordAccessField`.
        parent_owners = record.parent.access.owners
        parent_contributors = record.parent.access.contributors

        return parent_owners, parent_contributors


__all__ = (
    "UserInProject",
    "BaseIndexedProjectContextGenerator",
    "BaseRecordColaboratorGenerator",
    "ProjectRecordColaborator",
    "VersionedProjectRecordColaborator",
    "BaseStoredProjectContextGenerator",
)
