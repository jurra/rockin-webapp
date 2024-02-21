import pytest

from django.test import Client, RequestFactory

from django.contrib.auth.models import User

from crudapp.models import Well, Core, CoreChip


@pytest.fixture
def generic_data():
    return {"date_time": '2021-06-22 13:00:00',
            "remarks": "Test Remarks",
            "lithology": "Test Lithology",
            }


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
def non_auth_client():
    # The client needs to be logged in to access the views
    client = Client()
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
        "core_section_number": 1,  # Should be a counter
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
        core_section_number=1,  # Should be a counter
        top_depth=100.00,
        planned_core_number="C1",
    )


