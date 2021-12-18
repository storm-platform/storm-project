# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.resources import RecordResourceConfig


class ResearchProjectResourceConfig(RecordResourceConfig):
    """Research Project resource configuration."""

    # Used to control two different route
    # prefixes with the same resource (general and user-specific)
    # as defined below.
    url_prefix = ""
    blueprint_name = "storm_research_projects"

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
    }


__all__ = "ResearchProjectResourceConfig"
