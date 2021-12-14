# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_permissions.generators import (
    AuthenticatedUser,
    SystemProcess,
)

from invenio_records_permissions.policies import BasePermissionPolicy
from storm_project.project.services.security.generators import (
    ResearchProjectOwner,
    ResearchProjectContributor,
)


class ResearchProjectPermissionPolicy(BasePermissionPolicy):

    #
    # High level permissions
    #
    can_use = [ResearchProjectOwner(), ResearchProjectContributor(), SystemProcess()]

    can_manage = [ResearchProjectOwner(), SystemProcess()]

    #
    # Low level permissions
    #
    can_create = [AuthenticatedUser(), SystemProcess()]

    can_read = can_use

    can_update = can_manage

    can_delete = can_manage

    can_search = can_use

    can_search_user_project_research = [ResearchProjectOwner(), SystemProcess()]
