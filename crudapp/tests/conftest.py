import pytest

from crudapp.models import Well
from crudapp.models import Core

@pytest.fixture
def well():
    well = Well.objects.create(well_name="Test Well")
    return well

@pytest.fixture
def core_data(well):
    return {
        "registration_date": "2021-06-22 13:00:00",
        # "well_name": "Test Well", # This is correct for a view, but not for a model
        "well_id": well.id,
        "registered_by": "John Doe",
        "collection_date": "2021-06-22 12:00:00",
        "remarks": "Test Remarks",
        "drilling_mud": "Water-based mud",
        "lithology": "Test Lithology",
        "core_number": "C1",
        "core_section_number": 1, # Should be a counter
        "top_depth": 100.00,
    }
