# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import re

from invenio_records.dictutils import dict_set

from marshmallow import ValidationError


from invenio_access.permissions import system_process

from invenio_pidstore.errors import PIDAlreadyExists
from invenio_records_resources.services.records.components import ServiceComponent


class PIDComponent(ServiceComponent):
    """PID generator component.

    See:
        This class is adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/services/components.py#L18
    """

    @classmethod
    def _validate(cls, pid_value):
        """Checks the validity of the provided pid value."""
        blop = re.compile("^[-\w]+$")
        if not bool(blop.match(pid_value)):
            raise ValidationError(
                "The ID should contain only letters with numbers or dashes.",
                field_name="id",
            )

    def create(self, identity, record=None, data=None, **kwargs):
        """Create a Research Project PID from its metadata."""
        data["id"] = data["id"].lower()
        self._validate(data["id"])
        record["id"] = data["id"]
        try:
            provider = record.__class__.pid.field._provider.create(record=record)
        except PIDAlreadyExists:
            raise ValidationError(
                "A Research Project with this identifier already exists.",
                field_name="id",
            )
        setattr(record, "pid", provider.pid)


class ResearchProjectAccessComponent(ServiceComponent):
    """Access component to Research Project.

    See:
        This code is adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/services/components.py#L126
    """

    def _populate_access_and_validate(self, identity, data, record, **kwargs):
        if record is not None and "access" in data:
            record.setdefault("access", {})
            record["access"].update(data.get("access", {}))

    def _init_owners(self, identity, record, **kwargs):
        """Create a owner field into the record metadata."""
        is_system_process = system_process in identity.provides

        owners = []
        if not is_system_process:
            owners = [{"user": identity.id}]

        dict_set(record, "access.owned_by", owners)

    def _init_contributors(self, identity, record, **kwargs):
        """Create a contributor field into the record metadata."""
        is_system_process = system_process in identity.provides

        contributors = []
        if not is_system_process:
            contributors = [{"user": identity.id}]

        dict_set(record, "access.contributed_by", contributors)

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        self._populate_access_and_validate(identity, data, record, **kwargs)
        self._init_owners(identity, record, **kwargs)
        self._init_contributors(identity, record, **kwargs)

    def update(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access_and_validate(identity, data, record, **kwargs)

    def update_draft(self, identity, data=None, record=None, **kwargs):
        """Update handler."""
        self._populate_access_and_validate(identity, data, record, **kwargs)

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        record.access = draft.access

    def edit(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.access = record.access

    def new_version(self, identity, draft=None, record=None, **kwargs):
        """Update draft metadata."""
        draft.access = record.access


__all__ = ("PIDComponent", "ResearchProjectAccessComponent")
