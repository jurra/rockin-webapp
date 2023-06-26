import pytest

from crudapp.models import Well
from crudapp.models import Core

@pytest.fixture
def well():
    # This is currently not simulating a payload from the frontend
    well = Well.objects.create(name="Test Well")
    return well

@pytest.fixture
def core_data(well):
    # This is currently not simulating a payload from the frontend
    return {
        "registration_date": "2021-06-22 13:00:00",
        "core_type": "Core",
        "well": well,
        "registered_by": "John Doe",
        "collection_date": "2021-06-22 12:00:00",
        "remarks": "Test Remarks",
        "drilling_mud": "Water-based mud",
        "lithology": "Test Lithology",
        "core_number": "C1",
        "core_section_number": 1, # Should be a counter
        "top_depth": 100.00,
        "planned_core_number": "C1",
        "core_section_name": "Test Well-C1-1"
    }

@pytest.fixture
def invalid_date_time(well, core_data):
    core_data["registration_date"] = '2021-06-22'

@pytest.fixture
def core(well):
    return Core.objects.create(
        well=well,
        registration_date="2021-06-22 13:00:00",
        registered_by="John Doe",
        collection_date="2021-06-22 12:00:00",
        remarks="Test Remarks",
        drilling_mud="Water-based mud",
        lithology="Test Lithology",
        core_number="C1",
        core_section_number=1, # Should be a counter
        top_depth=100.00,
    )

