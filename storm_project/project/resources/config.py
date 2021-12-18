# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import marshmallow as ma
from invenio_records_resources.resources import RecordResourceConfig


class ResearchProjectResourceConfig(RecordResourceConfig):
    """Research Project resource configuration."""

    # we define the ``url_prefix`` as blank to control two different route
    # prefixes with the same resource (general and user-specific)
    # as defined below.
    url_prefix = ""
    blueprint_name = "storm_research_projects"

    # Request/Response configuration.
    request_view_args = {
        "user_type": ma.fields.String(
            validate=ma.fields.validate.OneOf(choices=["contributor", "owner"])
        ),
        "user_id": ma.fields.Int(),
        "pid_value": ma.fields.Str(),
    }

    routes = {
        # Routes prefix
        "projects-prefix": "/projects",
        "projects-user-prefix": "/user/projects",
        # Base operations
        "list": "",
        "base": "",
        "item": "/<pid_value>",
        # Status control
        "finish-item": "/<pid_value>/actions/finish",
        # Access control
        "list-item-agent": "/<pid_value>/admin/agents",
        "add-item-agent": "/<pid_value>/admin/actions/add/<user_type>/<user_id>",
        "remove-item-agent": "/<pid_value>/admin/actions/remove/<user_type>/<user_id>",
    }


__all__ = "ResearchProjectResourceConfig"
