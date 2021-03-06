# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_project.project.records.api import ResearchProject
from storm_project.project.schema import ResearchProjectSchema

from storm_project.project.services.security.permissions import (
    ResearchProjectPermissionPolicy,
)

from storm_commons.services.components import (
    CustomPIDGeneratorComponent,
    FinishStatusComponent,
)
from storm_project.project.services.components import ProjectAccessDefinitionComponent

from invenio_records_resources.services.records.config import RecordServiceConfig
from invenio_records_resources.services.records.components import MetadataComponent

from invenio_records_resources.services.records.links import (
    RecordLink,
    pagination_links,
)


def is_not_finished(record, ctx):
    """Check if the project is not finished."""
    return not record.is_finished


class ResearchProjectServiceConfig(RecordServiceConfig):
    """ResearchProject service configuration."""

    #
    # Common configurations
    #
    permission_policy_cls = ResearchProjectPermissionPolicy

    #
    # Record configuration
    #
    record_cls = ResearchProject

    schema = ResearchProjectSchema

    #
    # Service configuration
    #
    links_item = {"self": RecordLink("{+api}/projects/{id}")}

    links_action = {
        "finish": RecordLink(
            "{+api}/projects/{id}/actions/finish", when=is_not_finished
        ),
    }

    links_search = pagination_links("{+api}/projects{?args*}")
    links_search_user = pagination_links("{+api}/user/projects{?args*}")

    #
    # Components configuration
    #
    components = [
        MetadataComponent,
        ProjectAccessDefinitionComponent,
        CustomPIDGeneratorComponent,
        FinishStatusComponent,
    ]


__all__ = "ResearchProjectServiceConfig"
