# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_records.systemfields import ConstantField, DictField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField, PIDField

from .models import ResearchProjectMetadata
from .providers import ResearchProjectIdProvider


class ResearchProject(Record):
    """ResearchProject API."""

    pid = PIDField("id", provider=ResearchProjectIdProvider, create=False)
    schema = ConstantField("$schema", "local://projects/projects-v1.0.0.json")

    model_cls = ResearchProjectMetadata

    index = IndexField("projects-projects-v1.0.0", search_alias="projects")

    is_finished = DictField("is_finished")


__all__ = "ResearchProject"
