# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.services.records.components import ServiceComponent


class ProjectAccessDefinitionComponent(ServiceComponent):
    """Access component for projects.

    This component defines the access field of the project. Since the project
    have a special case in the access, we don’t use the storm-commons
    components (Only in this case).
    """

    def create(self, identity, data=None, record=None, **kwargs):
        """Add basic ownership fields to the record."""
        if record:
            _user_obj = {"user": identity.id}

            record.access.owners.append(_user_obj)
            record.access.contributors.append(_user_obj)
