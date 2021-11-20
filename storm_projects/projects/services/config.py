# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from .components import PIDComponent, ResearchProjectAccessComponent
from .permissions import ResearchProjectPermissionPolicy
from ..schema import ResearchProjectSchema

from ..records.api import ResearchProject

from invenio_records_resources.services.records.config import RecordServiceConfig
from invenio_records_resources.services.records.components import MetadataComponent

from invenio_records_resources.services.records.links import (
    RecordLink,
    pagination_links,
)


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

    links_search = pagination_links("{+api}/projects{?args*}")
    links_search_user = pagination_links("{+api}/user/projects{?args*}")

    #
    # Components configuration
    #
    components = [
        MetadataComponent,
        PIDComponent,
        ResearchProjectAccessComponent,
    ]


__all__ = "ResearchProjectServiceConfig"
