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

from invenio_access import superuser_access
from invenio_records_permissions.policies import BasePermissionPolicy

from storm_commons.services.generators import IfFinished
from storm_project.project.services.security.generators import (
    ResearchProjectOwner,
    ResearchProjectContributor,
)


class ResearchProjectPermissionPolicy(BasePermissionPolicy):

    #
    # High level permissions
    #

    # special case: the project entity have two types of users:
    #   - Owners;
    #   - Colaborators;
    # The ``Owners`` can manage the project (Update metadata, delete, and so on). Besides,
    # the ``Colaborators`` only are in the project context. So, they can't change the project.
    can_use = [ResearchProjectOwner(), ResearchProjectContributor(), SystemProcess()]

    can_admin = [ResearchProjectOwner(), SystemProcess()]
    can_manage = [IfFinished("is_finished", then_=[superuser_access], else_=can_admin)]

    #
    # Low level permissions
    #
    can_create = [AuthenticatedUser(), SystemProcess()]

    # Management actions
    can_update = can_manage
    can_delete = can_manage
    can_finish = can_manage

    # Read/Explore actions
    can_read = can_use
    can_search = can_use
    can_search_user_project_research = can_use
