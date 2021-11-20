# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-projects is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import current_app
from werkzeug.local import LocalProxy


current_research_project = LocalProxy(lambda: current_app.extensions["storm-projects"])
