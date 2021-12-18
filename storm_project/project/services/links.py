# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import request

from invenio_records_resources.services import Link, FileLink


class ProjectContextLink(Link):
    """Short cut for writing links with the Project context."""

    @staticmethod
    def vars(record, vars):
        """Variables for the URI template."""

        # project context: All endpoints is defined inside a project.
        # To maintain API consistency, the requested project is
        # used to filter the data and defined in the pagination links.
        project_id = request.view_args.get("project_id")

        # since we can receive different types of record, we need to
        # check some attributes before get the id value.
        if hasattr(record, "pid"):  # unique id value
            id_ = record.pid.pid_value
        else:
            id_ = record.id

        vars.update(
            {
                "id": id_,
                "project_id": project_id,
            }
        )


class ProjectContextFileLink(FileLink):
    """Short cut for writing file links with the Project context."""

    @staticmethod
    def vars(file_record, vars):
        """Variables for the URI template."""

        # project context: Loading the project context
        project_id = request.view_args.get("project_id")

        vars.update(
            {
                "key": file_record.key,
                "project_id": project_id,
            }
        )


class ProjectContextPaginationLink(Link):
    """Short cut for writing Project context pagination links."""

    def expand(self, obj, context):
        """Expand the URI Template."""

        # project context: Loading the project context
        project_id = request.view_args.get("project_id")

        context = {**context, "project_id": project_id}
        return super().expand(obj, context)


def project_context_pagination_links(tpl):
    """Create pagination links (prev/self/next) from the same template."""
    return {
        "prev": ProjectContextPaginationLink(
            tpl,
            when=lambda pagination, ctx: pagination.has_prev,
            vars=lambda pagination, vars: vars["args"].update(
                {"page": pagination.prev_page.page}
            ),
        ),
        "self": ProjectContextPaginationLink(tpl),
        "next": ProjectContextPaginationLink(
            tpl,
            when=lambda pagination, ctx: pagination.has_next,
            vars=lambda pagination, vars: vars["args"].update(
                {"page": pagination.next_page.page}
            ),
        ),
    }


__all__ = (
    "ProjectContextLink",
    "ProjectContextPaginationLink",
    "ProjectContextFileLink",
    "project_context_pagination_links",
)
