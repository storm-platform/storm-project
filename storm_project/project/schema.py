# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
    post_load,
)
from marshmallow_utils.fields import (
    NestedAttribute,
    SanitizedUnicode,
    EDTFDateString,
)

from marshmallow_utils.schemas import GeometryObjectSchema

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


def geo_names_valid(identifier):
    """Always validate JSON content."""
    return True


class Agent(Schema):
    """An agent schema.
    Note:
        This code is original from: https://github.com/inveniosoftware/invenio-rdm-records/blob/d7e7c7a2a44986de88e2d7941722bc72fd7dc345/invenio_rdm_records/services/schemas/parent/access.py#L42
    """

    user = fields.Integer(required=True)


class PersonOrOrganizationSchema(Schema):
    """Person or Organization schema.
    Note:
        This code is original from: https://github.com/inveniosoftware/invenio-rdm-records/blob/ccc3b19e9f18a0779c1f937a890196771a93b0fc/invenio_rdm_records/services/schemas/metadata.py#L114
    """

    NAMES = ["organizational", "personal"]

    type = SanitizedUnicode(
        required=True,
        validate=validate.OneOf(
            choices=NAMES,
            error="Invalid value. Choose one of {NAMES}.".format(NAMES=NAMES),
        ),
        error_messages={
            # [] needed to mirror error message above
            "required": ["Invalid value. Choose one of {NAMES}.".format(NAMES=NAMES)]
        },
    )
    name = SanitizedUnicode()
    given_name = SanitizedUnicode()
    family_name = SanitizedUnicode()

    @validates_schema
    def validate_names(self, data, **kwargs):
        """Validate names based on type."""
        if data["type"] == "personal":
            if not data.get("family_name"):
                messages = ["Family name must be filled."]
                raise ValidationError({"family_name": messages})

        elif data["type"] == "organizational":
            if not data.get("name"):
                messages = ["Name cannot be blank."]
                raise ValidationError({"name": messages})

    @post_load
    def update_names(self, data, **kwargs):
        """Update names for organization / person.
        Fill name from given_name and family_name if person.
        Remove given_name and family_name if organization.
        """
        if data["type"] == "personal":
            names = [data.get("family_name"), data.get("given_name")]
            data["name"] = ", ".join([n for n in names if n])

        elif data["type"] == "organizational":
            if "family_name" in data:
                del data["family_name"]
            if "given_name" in data:
                del data["given_name"]

        return data


class CreatorSchema(Schema):
    """Creator schema."""

    person_or_org = fields.Nested(PersonOrOrganizationSchema, required=True)


class ContributorSchema(Schema):
    """Contributor schema."""

    person_or_org = fields.Nested(PersonOrOrganizationSchema, required=True)


class DateSchema(Schema):
    """Schema for date intervals.

    Note:
        This code is original from: https://github.com/inveniosoftware/invenio-rdm-records/blob/ccc3b19e9f18a0779c1f937a890196771a93b0fc/invenio_rdm_records/services/schemas/metadata.py#L281
    """

    date = EDTFDateString(required=True)
    type = fields.Dict(required=True)
    description = fields.Str()


class LocationSchema(Schema):
    """Location schema.

    Note:
        This code is original from: https://github.com/inveniosoftware/invenio-rdm-records/blob/ccc3b19e9f18a0779c1f937a890196771a93b0fc/invenio_rdm_records/services/schemas/metadata.py#L374
    """

    place = SanitizedUnicode()
    description = SanitizedUnicode()
    geometry = fields.Nested(GeometryObjectSchema)

    @validates_schema
    def validate_data(self, data, **kwargs):
        """Validate identifier based on type."""
        if (
            not data.get("geometry")
            and not data.get("place")
            and not data.get("identifiers")
            and not data.get("description")
        ):
            raise ValidationError(
                {
                    "locations": (
                        "At least one of ['geometry', 'place', 'identifiers', 'description'] shold be present."
                    )
                }
            )


class FeatureSchema(Schema):
    """Location feature schema.

    See:
        This code is original from: https://github.com/inveniosoftware/invenio-rdm-records/blob/ccc3b19e9f18a0779c1f937a890196771a93b0fc/invenio_rdm_records/services/schemas/metadata.py
    """

    features = fields.List(fields.Nested(LocationSchema))


class ResearchProjectAccessSchema(Schema):
    """Research Project schema."""

    owned_by = fields.List(fields.Nested(Agent), required=False)
    contributed_by = fields.List(fields.Nested(Agent), required=False)


class ResearchProjectRightsSchema(Schema):
    """Research Project Rights schema."""

    id = fields.Str()
    title = fields.Str()
    description = fields.Str()

    link = fields.Str()


class ResearchProjectMetadataSchema(Schema):
    """Research project metadata field schema."""

    #
    # General descriptions
    #
    version = SanitizedUnicode()
    title = SanitizedUnicode(required=True, validate=_not_blank(max=250))
    description = SanitizedUnicode(validate=_not_blank(max=2000))

    subjects = fields.List(fields.Str())
    rights = fields.List(fields.Nested(ResearchProjectRightsSchema()))

    #
    # SpatioTemporal extent
    #
    locations = fields.Nested(FeatureSchema)
    dates = fields.List(fields.Nested(DateSchema))

    #
    # Creators and Contributors
    #
    creators = fields.List(fields.Nested(CreatorSchema))
    contributors = fields.List(fields.Nested(ContributorSchema))


class ResearchProjectSchema(BaseRecordSchema):
    """Schema for the Research Project metadata."""

    id = SanitizedUnicode(validate=_not_blank(max=100), required=True)
    metadata = NestedAttribute(ResearchProjectMetadataSchema, required=True)
    access = NestedAttribute(ResearchProjectAccessSchema, dump_only=True)


__all__ = "ResearchProjectSchema"
