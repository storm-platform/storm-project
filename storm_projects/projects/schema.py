# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_rdm_records.services.schemas.parent.access import Agent
from marshmallow import Schema, fields, validate
from marshmallow_utils.fields import NestedAttribute, SanitizedUnicode

from invenio_records_resources.services.records.schema import BaseRecordSchema


def _not_blank(**kwargs):
    """Returns a non-blank validation rule.

    See:
        This code was adapted from: https://github.com/inveniosoftware/invenio-communities/blob/837f33f1c0013a69fcec0ef188200a99fafddc47/invenio_communities/communities/schema.py#L21
    """
    max_ = kwargs.get("max", "")
    return validate.Length(
        error=f"Not empty string and less than {max_} characters allowed.",
        min=1,
        **kwargs,
    )


class ResearchProjectAccessSchema(Schema):
    owned_by = fields.List(fields.Nested(Agent), required=False)
    generated_by = fields.List(fields.Nested(Agent), required=False)


class ResearchProjectRightsSchema(Schema):
    id = fields.Str()
    title = fields.Str()
    description = fields.Str()

    link = fields.Str()


class ResearchProjectMetadataSchema(Schema):
    title = SanitizedUnicode(required=True, validate=_not_blank(max=250))
    description = SanitizedUnicode(validate=_not_blank(max=2000))

    subjects = fields.List(fields.Str())

    rights = fields.List(fields.Nested(ResearchProjectRightsSchema()))


class ResearchProjectSchema(BaseRecordSchema):
    """Schema for the Research Project metadata."""

    id = SanitizedUnicode(validate=_not_blank(max=100), required=True)
    metadata = NestedAttribute(ResearchProjectMetadataSchema, required=True)
    access = NestedAttribute(ResearchProjectAccessSchema, dump_only=True)


__all__ = "ResearchProjectSchema"
