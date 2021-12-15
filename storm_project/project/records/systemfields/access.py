# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_accounts.models import User as InvenioUser

from storm_commons.records.systemfields.models import Agent, AgentList
from storm_commons.records.systemfields.fields.access import RecordAccess


class ProjectAgent(Agent):
    """Project access agent."""

    #
    # Supported types
    #
    agent_cls = {"user": InvenioUser}  # projects don't have `project` agents.

    #
    # Loaders
    #
    agent_cls_loaders = {
        "user": lambda x: InvenioUser.query.get(x),
    }


class ProjectAgents(AgentList):
    """A list of Project Agents."""

    agent_cls = ProjectAgent


class ProjectAccess(RecordAccess):
    """Project access management."""

    owners_cls = ProjectAgents
    contributors_cls = ProjectAgents
