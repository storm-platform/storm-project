# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Storm module that adds support for Projects."""

from . import config
from .projects.resources.config import ResearchProjectResourceConfig
from .projects.resources.resource import ResearchProjectResource
from .projects.services.config import ResearchProjectServiceConfig
from .projects.services.service import ResearchProjectService


class StormProjects(object):
    """storm-projects extension."""

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)

        app.extensions["storm-projects"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            # Configurations for the invenio-jsonschemas and invenio-records components
            if k.startswith("JSONSCHEMAS") or k.startswith("RECORDS"):
                app.config.setdefault(k, getattr(config, k))

            # Configurations for the storm-oauth
            if k.startswith("STORM_PROJECTS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize research project services."""
        self.research_project_service = ResearchProjectService(
            ResearchProjectServiceConfig
        )

    def init_resources(self, app):
        """Initialize research project resources."""
        self.research_project_resource = ResearchProjectResource(
            ResearchProjectResourceConfig, self.research_project_service
        )
