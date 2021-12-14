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
    blueprint_name = "research_project"

    routes = {
        # Routes prefix
        "projects-prefix": "/projects",
        "projects-user-prefix": "/user/projects",
        # Base operations
        "list": "",
        "base": "",
        "item": "/<pid_value>",
    }


__all__ = "ResearchProjectResourceConfig"
