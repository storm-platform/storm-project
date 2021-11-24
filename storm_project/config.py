# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Storm module that adds support for Research Projects."""

#
# invenio-jsonschemas configuration
#
JSONSCHEMAS_HOST = "local"

#
# invenio-records configuration
#
RECORDS_REFRESOLVER_CLS = "invenio_records.resolver.InvenioRefResolver"
"""Custom JSONSchemas ref resolver class."""

RECORDS_REFRESOLVER_STORE = "invenio_jsonschemas.proxies.current_refresolver_store"
"""JSONSchemas ref resolver store."""
