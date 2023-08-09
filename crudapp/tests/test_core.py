import copy

import pytest
from unittest.mock import patch

from django.core.exceptions import ValidationError

from django.test import RequestFactory
from django.urls import reverse_lazy

from django.db import connection
from django.urls import reverse
from django.test import Client
from crudapp.models import Core, Well   
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
def test_core_form_view_post(auth_client, well, user, core_data):
    # Create a POST request with form data
    request_url = reverse('cores')  # Replace 'cores' with the actual URL name of the view

    # Append query parameters to the success URL
    query_params = {
        'well_name': core_data['well'].name,
        'core_number': 'C1'
    }
    request_url += '?' + '&'.join([f'{key}={value}' for key, value in query_params.items()])

    data = {
        'registration_date': '2021-06-22 13:00:00',
        'core_type': 'Core',
        'well': well.name,  # Assuming well is an instance of the Well model
        'registered_by': 'testuser',
        'collection_date': '2021-06-22 12:00:00',
        'remarks': 'Test Remarks',
        'drilling_mud': 'Water-based mud',
        'lithology': 'Test Lithology',
        'core_number': 'C1',
        'core_section_number': 1,
        'top_depth': 100.0,
        'planned_core_number': 'C1',
        'core_section_name': 'Test Well-C1-1',
        'user': user.pk,  # Assuming user is an instance of the User model
    }

    auth_client.force_login(user)
    response = auth_client.post(request_url, data=data)

    assert response.status_code == 302
    assert Core.objects.filter(core_section_name=data['core_section_name']).exists()

    # Now we want to test invalid data
    data['well'] = 'Invalid Well'
    response = auth_client.post(request_url, data=data)
    assert response.context_data['form'].errors['well'] == ['Select a valid choice. That choice is not one of the available choices.']


# TODO: Test the sequence behaviour of core_catcher, cores and core_section_number
@pytest.mark.django_db
def test_core_catcher_sequence(core_data):
    pass


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
