import pytest

from crudapp.models.django_well import Well
from crudapp.models.django_core import Core

@pytest.fixture
def well():
    well = Well.objects.create(well_name="Test Well")
    return well

@pytest.fixture
def core(well):
    core = Core.objects.create(well=well, top_depth=100.00, bottom_depth=110.00)
    return core

@pytest.mark.django_db
def test_well_creation(well):
    assert well.well_name == "Test Well"

@pytest.mark.django_db
def test_core_creation(core):
    assert core.top_depth == 100.00
    assert core.bottom_depth == 110.00

@pytest.mark.django_db
def test_well_core_relationship(well, core):
    assert core.well == well
    assert well.cores.first() == core
