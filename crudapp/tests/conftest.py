import pytest

from django.test import Client, RequestFactory

from django.contrib.auth.models import User

from crudapp.models import Well, Core, CoreChip

@pytest.fixture
def session_key():
    return '_auth_user_id'

# Create a user object
@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="",
        password="testpassword"
    )

@pytest.fixture
def auth_client(user):
    # The client needs to be logged in to access the views
    client = Client()
    client.login(username=user.username, password=user.password)
    return client

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def well():
    # This is currently not simulating a payload from the frontend
    well = Well.objects.create(name="Test Well")
    return well


@pytest.fixture
def core_data(well, user):
    # This is currently not simulating a payload from the frontend
    return {
        "registration_date": "2021-06-22 13:00:00",
        "core_type": "Core",
        "well": well,
        "registered_by": user,
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
def core(well, user):
    return Core.objects.create(
        well=well,
        registration_date="2021-06-22 13:00:00",
        registered_by=user,
        collection_date="2021-06-22 12:00:00",
        remarks="Test Remarks",
        drilling_mud="Water-based mud",
        lithology="Test Lithology",
        core_number="C1",
        core_section_number=1, # Should be a counter
        top_depth=100.00,
        planned_core_number="C1",
    )

@pytest.fixture
def corechip(well, user, core):
    # Shorten the name as it is required for the corechip name
    well_name_short = well.gen_short_name()

    return CoreChip.objects.create(
        well=well,
        registration_date = '2021-06-22 13:00:00',
        collection_date='2021-06-22 12:00:00',
        core_number=core.core_number,
        core_section_number=core.core_section_number,
        planned_core_number=core.planned_core_number,
        corechip_number='2',
        drilling_mud='Water-based mud',
        registered_by=user,
        from_top_bottom='Top',  # Replace with the desired from_top_bottom choice
        corechip_name=well_name_short + '-C1-2-CHB7',  
        corechip_depth=10.0,  # Replace with the desired core_chip_depth
        lithology='Sample Lithology',
        remarks='Sample Remarks',
        debris=False,  # Replace with the desired debris value
        formation='Sample Formation',
        top_depth=100.0,  # Replace with the desired top_depth
    )

@pytest.fixture
def corechip_json(corechip, well):
    return  {
        # This is post data from the frontend
        'well': well.name,
        'well_name': well.name,
        'registration_date': corechip.registration_date,
        'registered_by': corechip.registered_by.id,
        'collection_date': corechip.collection_date,
        'core_number': corechip.core_number,
        'planned_core_number': corechip.planned_core_number,
        'core_section_number': corechip.core_section_number,
        'core_section_name': corechip.core_section_name,
        'drilling_mud': corechip.drilling_mud,
        'corechip_number': corechip.corechip_number,
        'from_top_bottom': corechip.from_top_bottom,
        'corechip_name': corechip.corechip_name,
        'corechip_depth': corechip.corechip_depth,
        'lithology': corechip.lithology,
        'remarks': corechip.remarks,
        'debris': corechip.debris,
        'formation': corechip.formation,
        'top_depth': corechip.top_depth,
        'core_type': 'Core'
    }