"""Semantic content layer — realistic names, attribute values, edge values."""

from .edge_values import materialize_edge_values
from .example_pools import build_instance
from .org_names import (
    ORG_EMPLOYEE_ATTRS,
    ORG_PERSON_ATTRS,
    ORG_TEAM_NAMES,
    generate_employee_attrs,
    generate_person_attrs,
    generate_team_attrs,
)

__all__ = [
    "build_instance",
    "materialize_edge_values",
    "ORG_PERSON_ATTRS",
    "ORG_EMPLOYEE_ATTRS",
    "ORG_TEAM_NAMES",
    "generate_person_attrs",
    "generate_employee_attrs",
    "generate_team_attrs",
]
