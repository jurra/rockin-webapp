import pytest
from django.core.exceptions import ValidationError


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

# @pytest.mark.django_db
# def test_well_core_relationship(well, core_data):
#     assert core_data.well == well
#     assert well.cores.first() == core_data

@pytest.mark.django_db
def test_well_cores_relationship(well,core_data):
    # Create two Core instances related to the same well
    core1 = Core.objects.create(**core_data)
    core2 = Core.objects.create(**core_data)

    core2.core_type = "Core catcher"

    assert core_data.well_id == well.id
    assert well.cores.first() == core_data

    # Assert that the related_name 'cores_well' returns the expected cores for the Well instance
    assert list(well.cores_well.all()) == [core1, core2]

    # Assert that the foreign key relationship between Core and Well is working correctly
    assert core1.well_id == well.id
    assert core2.well_id == well.id

#TODO: Test the sequence behaviour of core_catcher, cores and core_section_number

#TODO: Test counter behaviour of core_section_number