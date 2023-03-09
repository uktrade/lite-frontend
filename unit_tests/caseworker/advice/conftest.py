import pytest


@pytest.fixture
def with_lu_countersigning_enabled(settings):
    settings.FEATURE_LU_POST_CIRC_COUNTERSIGNING = True


@pytest.fixture
def with_lu_countersigning_disabled(settings):
    settings.FEATURE_LU_POST_CIRC_COUNTERSIGNING = False
