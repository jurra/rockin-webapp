import copy

import pytest
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.test import RequestFactory
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

# test core view


@pytest.mark.django_db
def test_core_form_view(core_data):
    request = RequestFactory().get(reverse('cores'))
    view = CoreFormView.as_view()
    response = view(request)

    # Test that the template used by the view is correct
    assert response.template_name == ['core.html']

    # Test that the form used by the view is correct
    assert isinstance(response.context_data['form'], CoreForm)

    # Test valid form submission
    form_data = copy.deepcopy(core_data)
    request = RequestFactory().post(reverse('cores'), data=form_data)
    response = view(request)

    assert response.status_code == 302  # Redirect to success_url
    assert Core.objects.filter(core_number=form_data['core_number']).exists()

    # Test invalid form submission
    existing_core = Core.objects.first()
    form_data = {'core_number': existing_core.core_number}
    request = RequestFactory().post(reverse('cores'), data=form_data)
    response = view(request)
    assert response.status_code == 200
    assert not response.context_data['form'].is_valid()


# TODO: Test the sequence behaviour of core_catcher, cores and core_section_number

# TODO: Test counter behaviour of core_section_number
