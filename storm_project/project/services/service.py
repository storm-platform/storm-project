# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from elasticsearch_dsl import Q
from invenio_records_resources.services import LinksTemplate

from invenio_records_resources.services.records import RecordService
from invenio_records_resources.services.uow import unit_of_work, RecordCommitOp


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

    @unit_of_work()
    def finish_project(self, identity, project_id, uow=None):
        """Finish a research project.

        Args:
            identity (flask_principal.Identity): User identity

            project_id (str): Research project id

        Returns:
            Dict: The updated Research Project document.
        """
        # loading the record
        record = self.record_cls.pid.resolve(project_id)

        # checking permissions
        self.require_permission(identity, "finish", record=record)

        self.run_components(
            "finish",
            identity,
            record=record,
            uow=uow,
        )

        # Persist record (DB and index)
        uow.register(RecordCommitOp(record, self.indexer))

        return self.result_item(self, identity, record, links_tpl=self.links_item_tpl)


__all__ = "ResearchProjectService"
