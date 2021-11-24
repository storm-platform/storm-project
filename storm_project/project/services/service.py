# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from elasticsearch_dsl import Q
from invenio_records_resources.services import LinksTemplate

from invenio_records_resources.services.records import RecordService


class ResearchProjectService(RecordService):
    """Research project service."""

    def __init__(self, config):
        super(ResearchProjectService, self).__init__(config)

    def search_user_research_projects(
        self, identity, params=None, es_preference=None, **kwargs
    ):
        """Search for user Research Project."""
        self.require_permission(identity, "search_user_project_research")

        # preparing the search operator (record or contributor)
        extra_filter = Q("term", **{"access.owned_by.user": identity.id}) | Q(
            "term", **{"access.contributed_by.user": identity.id}
        )

        params = params or {}
        search_result = self._search(
            "search",
            identity,
            params,
            es_preference,
            extra_filter=extra_filter,
            permission_action="read",
            **kwargs
        ).execute()

        return self.result_list(
            self,
            identity,
            search_result,
            params,
            links_tpl=LinksTemplate(
                self.config.links_search_user, context={"args": params}
            ),
            links_item_tpl=self.links_item_tpl,
        )


__all__ = "ResearchProjectService"
