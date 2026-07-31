from __future__ import annotations

from copy import deepcopy

import pytest

from pragmatic.io import load_method, load_yaml


@pytest.fixture
def method():
    return load_method()


@pytest.fixture
def complete_document():
    return deepcopy(load_yaml("examples/complete-objective.yaml"))
