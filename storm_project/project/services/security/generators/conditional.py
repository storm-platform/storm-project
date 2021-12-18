# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pydash import py_

from storm_project.proxies import current_project
from storm_commons.services.generators import BaseConditionalGenerator


class IfProjectFinished(BaseConditionalGenerator):
    """IfProjectFinished generator.

    This conditional generator check if the current project is finished:

        IfProjectFinished(
            then_ = [<Generator>, <Generator>,],
            else_ = [<Generator>, <Generator>]
        )
    """

    def __init__(self, then_, else_):
        self.then_ = then_
        self.else_ = else_

    def generators(self, record):
        """Choose between 'then' or 'else' generators."""
        return self.then_ if current_project.data.get("is_finished") else self.else_


class IfRecordOrProjectFinished(BaseConditionalGenerator):
    """IfRecordOrProjectFinished generator.

    This conditional generator check if a record or they associated project are
    finished (based on an arbitrary field):

        IfRecordOrProjectFinished(
            field = 'is_finished',
            then_ = [<Generator>, <Generator>,],
            else_ = [<Generator>, <Generator>]
        )
    """

    def __init__(self, field, then_, else_):
        self.field = field
        self.then_ = then_
        self.else_ = else_

    def generators(self, record):
        """Choose between 'then' or 'else' generators."""
        if record:
            # checking for the project context

            # about the storm implementation: we need to check two types of records:
            #   1. ``Indexed`` in the elasticsearch, which have a json document;
            #   2. ``Stored`` only in the database, which have the project relationship in a table.
            if hasattr(record, "access"):
                # ``Indexed`` records
                is_project_finished = record.access.owned_by[0]._entity.json.get(
                    "is_finished"
                )
            else:
                # ``Stored`` records
                is_project_finished = record.project.json.get("is_finished")

            # getting the field using pydash
            # (handle properties and keys equally)
            is_record_finished = py_.get(record, self.field)

        else:
            # record is none, we only check the project context.
            # note: in the ``if`` statement, we don't use the ``current_project``
            # to avoid some database queries. This will change in the future.
            is_record_finished = False
            is_project_finished = current_project.data.get("is_finished")

        if any([is_project_finished, is_record_finished]):
            return self.then_
        return self.else_
