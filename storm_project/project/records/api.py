# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from invenio_records_resources.records.api import Record
from invenio_records.systemfields import ConstantField, DictField
from invenio_records_resources.records.systemfields import IndexField, PIDField

from storm_project.project.records.models import ResearchProjectMetadata
from storm_project.project.records.providers import ResearchProjectIdProvider


class ResearchProject(Record):
    """ResearchProject High-level API."""

    pid = PIDField("id", provider=ResearchProjectIdProvider, create=False)
    schema = ConstantField("$schema", "local://project/project-v1.0.0.json")

    model_cls = ResearchProjectMetadata

    index = IndexField("project-project-v1.0.0", search_alias="project")

    is_finished = DictField("is_finished")


__all__ = "ResearchProject"
