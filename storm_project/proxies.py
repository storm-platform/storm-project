# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request

from flask import current_app
from werkzeug.local import LocalProxy


current_research_project_extension = LocalProxy(
    lambda: current_app.extensions["storm-project"]
)
"""Research project extension proxy."""


def _current_project():
    """Retrieve the current project."""
    from flask import g

    project_obj = None
    project_id = request.view_args.get("project_id", None)

    if project_id:
        project_obj = current_research_project_extension.research_project_service.read(
            project_id, g.identity
        )

    return project_obj


current_project = LocalProxy(_current_project)
"""Current project instance proxy."""

__all__ = ("current_project", "current_research_project_extension")
