import copy

import pytest
from unittest.mock import patch

from django.core.exceptions import ValidationError

from django.db import connection
from django.urls import reverse
from django.test import Client
from crudapp.models import Core
from crudapp.forms import CoreForm
from crudapp.views import CoreFormView

# TEST CORE MODEL
@pytest.mark.django_db
def test_core_fields(core_data):
    core = Core.objects.create(**core_data)
    assert core.registration_date == core_data["registration_date"]
    assert core.well == core_data["well"]
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
    # FIXME: This should be tested on the pydantic model not directly via the ORM
    # Test if creating Core objects without required fields raises validation errors
    core = Core.objects.create(**core_data)
    with pytest.raises(ValidationError):
        core.registration_date = "2021-06-2"

    with pytest.raises(ValidationError):
        Core.objects.create(well_name="Test Well")

    with pytest.raises(ValidationError):
        Core.objects.create(collection_date="2021-06-22")

    with pytest.raises(ValidationError):
        Core.objects.create(core_number="C1")

    with pytest.raises(ValidationError):
        Core.objects.create(core_section_number=1)

    with pytest.raises(ValidationError):
        Core.objects.create(core_section_name="Test Well C1 - Section 1")

# Test core name generation
@pytest.mark.django_db
def test_core_creation(core_data):
    '''
    AC: The core_section_name should be generated automatically based on the following fields:
    - well.name
    - core_number
    - core_section_number    
    '''
    # Assert that the core_section_name is generated correctly
    core = Core.objects.create(**core_data)
    core_section_name_units = [
        core_data['well'].name, str(core_data['core_number']), str(core_data['core_section_number'])]

    expected_core_section_name = "-".join(core_section_name_units)
    assert core.core_section_name == expected_core_section_name


@pytest.mark.django_db
def test_well_cores_relationship(well, core_data):
    '''
    AC: A Core should be related to a Well.
    AC: The Well instance should be able to access the Core instances that are related to it
    AC: The Core instance should be able to access the Well instance that it is related to
    '''
    core1 = Core.objects.create(**core_data)
    core2 = Core.objects.create(**core_data)

    # Update core2 in the database
    Core.objects.filter(pk=core2.pk).update(core_type="Core catcher")

    assert core1.well == well
    assert well.cores.first() == core1

    # Assert that the related_name 'cores_well' returns the expected cores for the Well instance
    assert list(well.cores.all()) == [core1, core2]
    assert list(well.cores.values_list('pk', flat=True)) == [
        core1.pk, core2.pk]

    # Assert that the foreign key relationship between Core and Well is working correctly
    assert core1.well == well
    assert core2.well == well

    # assert that core1 section name is correctly generated
    # assert that core2 section name respects the sequence pattern... counting

@pytest.mark.django_db
def test_core_form_view_get_initial(well, request_factory):
    print(f"This is the test well: {well.pk}")
    view = CoreFormView()
    
    # The request url should be this one:/wells/1/cores/create/?well_name=DAP&core_number=C1
    # Build request so that it resembles the one above
    request = request_factory.get(reverse('cores'), {'well_name': well.name, 'core_number': 'C1'})
    view.request = request

    view.kwargs = {'pk': well.pk, 'well': well.name}  
    initial = view.get_initial()

    assert 'collection_date' in initial
    assert 'well' in initial
    assert 'core_number' in initial

@pytest.mark.django_db
@patch('crudapp.views.CoreFormView.get_initial')
def test_core_form_view_post(mock_get_initial,auth_client, well, core_data, request_factory, user):
    auth_client.force_login(user)

    # Create a POST request with query parameters
    url = reverse('cores')  # Replace 'core_form' with the actual URL name of the view

    data = core_data
    assert core_data['well'].name == well.name
    assert core_data['well'].pk == well.pk

    data['well'] = well.pk

    request = request_factory.post(url, data=data)
    request.user = user
    assert request.user == user   

    # Mock the behavior of get_initial method
    mock_initial_values = {
        'collection_date': core_data['collection_date'],
        'well': core_data['well'],
        'core_number': core_data['core_number'],
        'core_section_number': core_data['core_section_number'],
    }

    mock_get_initial.return_value = mock_initial_values

    # Instantiate and process the view
    view = CoreFormView.as_view()
    view.request = request
    print(f"This is the view.request: {dir(view.request)}")
    response = auth_client.post(view.request.path)

    assert response.status_code == 200


@pytest.mark.django_db
def test_core_form_view(core_data, user, request_factory):
    # Create a Client instance for handling requests
    client = Client()

    # Log in the user
    client.force_login(user)
    well = core_data['well']
    view = CoreFormView.as_view()
    response = client.get(reverse('cores'), {'well_name': well.name, 'core_number': 'C1'})

    # Test that the template used by the view is correct
    assert response.template_name == ['core.html']

    # Test that the form used by the view is correct
    assert isinstance(response.context_data['form'], CoreForm)

    # Test valid form submission
    response = client.post(reverse('cores'), data=form_data)

    assert response.status_code == 302  # Redirect to success_url
    assert Core.objects.filter(core_number=form_data['core_number']).exists()

    # Test invalid form submission
    existing_core = Core.objects.first()
    form_data = {'core_number': existing_core.core_number}
    request = request_factory.post(reverse('cores'), data=form_data)
    response = view(request)
    assert response.status_code == 200
    assert not response.context_data['form'].is_valid()


# TODO: Test the sequence behaviour of core_catcher, cores and core_section_number
@pytest.mark.django_db
def test_core_catcher_sequence(core_data):
    pass


# TODO: Test counter behaviour of core_section_number
@pytest.mark.django_db
def test_core_section_number_counter(core_data):
    '''Create in the following sequence:
    1. Core
    2. Core catcher
    3. Core
    '''
    # AC: Check that the core catcher last number is one more than the last core number
    
    # AC: Check that the core last number is one more than the last core catcher number
    pass
