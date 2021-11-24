# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


def create_research_project_blueprint_api(app):
    """Create Research Project API Blueprint."""
    ext = app.extensions["storm-project"]

    return ext.research_project_resource.as_blueprint()


__all__ = "create_research_project_blueprint_api"
