# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from invenio_db import db
from invenio_records.models import RecordMetadataBase


class ResearchProjectMetadata(db.Model, RecordMetadataBase):
    """Research project database model."""

    __tablename__ = "research_projects"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}


__all__ = "ResearchProjectMetadata"
