# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Storm module that adds support for Projects."""

from .ext import StormProject
from .version import __version__

from .proxies import current_project, current_research_project_extension

__all__ = (
    # Extension constructor
    "StormProject",
    # Proxies
    "current_project",
    "current_research_project_extension",
    # Package metadata
    "__version__",
)
