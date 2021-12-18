# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import g
from flask_resources import route, response_handler, resource_requestctx

from invenio_records_resources.resources.records.utils import es_preference

from storm_commons.admin.resource import AdminRecordResource
from storm_commons.resources.parsers import request_view_args, request_search_args


class ResearchProjectResource(AdminRecordResource):
    """Research project API resource."""

    def create_url_rules(self):
        """Routing for the views."""

        def join_url(prefix, route):
            """Auxiliary function for URL concat."""
            return f"{prefix}{route}"

        routes = self.config.routes
        url_rules = [
            route(
                "POST", join_url(routes["projects-prefix"], routes["base"]), self.create
            ),
            route(
                "GET", join_url(routes["projects-prefix"], routes["item"]), self.read
            ),
            route(
                "GET", join_url(routes["projects-prefix"], routes["list"]), self.search
            ),
            route(
                "PUT", join_url(routes["projects-prefix"], routes["item"]), self.update
            ),
            route(
                "DELETE",
                join_url(routes["projects-prefix"], routes["item"]),
                self.delete,
            ),
            route(
                "GET",
                join_url(routes["projects-user-prefix"], routes["list"]),
                self.search_user_research_projects,
            ),
            # Status control
            route(
                "POST",
                join_url(routes["projects-prefix"], routes["finish-item"]),
                self.finish_project,
            ),
            # Access control
            route(
                "POST",
                join_url(routes["projects-prefix"], routes["add-item-agent"]),
                self.admin_add_agent,
            ),
            route(
                "DELETE",
                join_url(routes["projects-prefix"], routes["remove-item-agent"]),
                self.admin_remove_agent,
            ),
            route(
                "GET",
                join_url(routes["projects-prefix"], routes["list-item-agent"]),
                self.admin_list_agents,
            ),
        ]

        return url_rules

    @request_search_args
    @response_handler(many=True)
    def search_user_research_projects(self):
        """Search for Research projects related to a authenticated user.

        See:
            This code was adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/resources/resource.py#L86
        """
        hits = self.service.search_user_research_projects(
            identity=g.identity,
            params=resource_requestctx.args,
            es_preference=es_preference(),
        )

        return hits.to_dict(), 200

    @request_view_args
    @response_handler()
    def finish_project(self):
        """Finish a research project."""
        edited_project = self.service.finish_project(
            g.identity,
            resource_requestctx.view_args["pid_value"],
        )
        return edited_project.to_dict(), 200
