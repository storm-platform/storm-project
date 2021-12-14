# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_commons.records.providers import RegisteredIdProvider


class ResearchProjectIdProvider(RegisteredIdProvider):
    """Research project PID provider."""

    pid_type = "projid"


__all__ = "ResearchProjectIdProvider"
