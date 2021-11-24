# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-project is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Storm module that adds support for Project."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "pytest-invenio>=1.4.0",
]

extras_require = {
    "docs": [
        "Sphinx>=3,<4",
    ],
    "tests": tests_require,
}

extras_require["all"] = [req for _, reqs in extras_require.items() for req in reqs]

setup_requires = [
    "Babel>=2.8",
]

install_requires = [
    "invenio-i18n>=1.2.0",
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("storm_project", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="storm-project",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords=["Storm Platform", "Research projects", "Invenio module"],
    license="MIT",
    author="Felipe Menino Carlos",
    author_email="felipe.carlos@inpe.br",
    url="https://github.com/storm-platform/storm-project",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={
        "invenio_config.module": [
            "storm_project = storm_project.config",
        ],
        "invenio_base.apps": [
            "storm_project = storm_project:StormProject",
        ],
        "invenio_base.api_apps": [
            "storm_project = storm_project:StormProject",
        ],
        "invenio_base.api_blueprints": [
            "storm_project_api = storm_project.views:create_research_project_blueprint_api"
        ],
        "invenio_db.models": [
            "storm_project = storm_project.project.records.models"
        ],
        "invenio_search.mappings": [
            "project = storm_project.project.records.mappings"
        ],
        "invenio_jsonschemas.schemas": [
            "project = storm_project.project.records.jsonschemas"
        ]
        # 'invenio_access.actions': [],
        # 'invenio_admin.actions': [],
        # 'invenio_assets.bundles': [],
        # 'invenio_base.api_apps': [],
        # 'invenio_base.api_blueprints': [],
        # 'invenio_base.blueprints': [],
        # 'invenio_celery.tasks': [],
        # 'invenio_db.models': [],
        # 'invenio_pidstore.minters': [],
        # 'invenio_records.jsonresolver': [],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
    ],
)
