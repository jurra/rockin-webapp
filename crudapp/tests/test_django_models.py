import pytest
from django.core.exceptions import ValidationError


from crudapp.models import Well
from crudapp.models import Core

@pytest.fixture
def well():
    well = Well.objects.create(well_name="Test Well")
    return well

@pytest.fixture
def core_data():
    return {
        "registration_date": "2021-06-22 13:00:00",
        "well_name": "Test Well",
        "registered_by": "John Doe",
        "collection_date": "2021-06-22 12:00:00",
        "remarks": "Test Remarks",
        "drilling_mud": "Water-based mud",
        "lithology": "Test Lithology",
        "core_number": "C1",
        "core_section_number": 1,
        "core_section_name": "Test Well C1 - Section 1",
        "top_depth": 100.00,
        "core_section_number": 1, # This should be a counter
    }

@pytest.mark.django_db
def test_well_creation(well):
    assert well.well_name == "Test Well"

@pytest.mark.django_db
def test_core_fields(core_data):
    core = Core.objects.create(**core_data)
    assert core.registration_date == core_data["registration_date"]
    assert core.well_name == core_data["well_name"]
    assert core.registered_by == core_data["registered_by"]
    assert core.collection_date == core_data["collection_date"]
    assert core.remarks == core_data["remarks"]
    assert core.drilling_mud == core_data["drilling_mud"]
    assert core.lithology == core_data["lithology"]
    assert core.core_number == core_data["core_number"]
    assert core.core_section_number == core_data["core_section_number"]
    assert core.core_section_name == core_data["core_section_name"]

@pytest.mark.django_db
def test_core_invalid_fields(core_data):
    # Test if creating Core objects without required fields raises validation errors
    core = Core.objects.create(**core_data)
    with pytest.raises(ValidationError):
        core.registration_date = "2021-06-22 13:00:00"

    with pytest.raises(ValidationError):
        Core.objects.create(well_name="Test Well")

    with pytest.raises(ValidationError):
        Core.objects.create(collection_date="2021-06-22 12:00:00")

    with pytest.raises(ValidationError):
        Core.objects.create(core_number="C1")

    with pytest.raises(ValidationError):
        Core.objects.create(core_section_number=1)

    with pytest.raises(ValidationError):
        Core.objects.create(core_section_name="Test Well C1 - Section 1")

@pytest.mark.django_db
def test_well_core_relationship(well, core_data):
    assert core_data.well == well
    assert well.cores.first() == core_data
