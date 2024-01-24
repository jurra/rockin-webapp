import copy
import json
from pprint import pprint

import pytest
from pydantic import ValidationError

from crudapp.models import MicroCore
from crudapp.views import _validate

from django.urls import reverse
from django.forms.models import model_to_dict
from django.db import IntegrityError

from datamodel import MicroCore as MicroCoreModel
from crudapp.views import MicroCoreFormView

@pytest.fixture
def microcore_object(core, well, user, generic_data):
    # Microcore object cannot be duplicate
    microcore_number = 1

    return MicroCore.objects.create(
        well=well,
        registered_by=user,
        collection_date=generic_data['date_time'],
        remarks=generic_data['remarks'],
        drilling_mud="Oil-based mud",
        lithology=generic_data['lithology'],
        micro_core_number=microcore_number,
        micro_core_name=f"{well.gen_short_name()}-MC-{microcore_number}",
        drilling_method="Rotary",
        drilling_bit="Test Bit",
    )


@pytest.fixture
def microcore_json(microcore_object, generic_data):
    serialized = model_to_dict(microcore_object)
    serialized['registration_date'] = generic_data['date_time'] # this needs to be added because it is excluded in the model_to_dict
    return serialized

@pytest.fixture
def invalid_microcore_json(microcore_json):
    invalid = copy.deepcopy(microcore_json)
    invalid['drilling_mud'] = 'Test Mud'
    invalid['registered_by'] = ''
    invalid['well'] = 'invalid_key'

    return invalid


@pytest.mark.django_db
def test_microcore_data(microcore_json):
    assert microcore_json['micro_core_name'] == 'TestWell-MC-1'


# TEST MODEL
@pytest.mark.django_db
def test_create_microcore(microcore_json, well, user):
    '''
    AC: Micro name cannot be duplicate
    '''
    # Create a duplicate instance
    duplicate_microcore = copy.deepcopy(microcore_json)

    duplicate_microcore['well'] = well
    duplicate_microcore['registered_by'] = user

    assert MicroCore.objects.count() == 1
    assert MicroCore.objects.first().micro_core_name == 'TestWell-MC-1'

    with pytest.raises(IntegrityError):
        # create a microcore instance by copypasting microcore
        MicroCore.objects.create(**duplicate_microcore)

# TEST VALIDATION
@pytest.mark.django_db
def test_validate_microcore(microcore_json, microcore_object):
    '''AC: Comply with pydantic model
    '''
    valid = _validate(microcore_json, model_name='MicroCore')
    assert isinstance(valid, MicroCoreModel)  # Check that a valid MicroCore object is returned
    # assert isinstance(valid, MicroCore)  # Check that a valid MicroCore object is returned

    # Create invalid data
    invalid_payload = copy.deepcopy(microcore_json)
    invalid_payload['drilling_mud'] = 'Test Mud'
    invalid_payload['registered_by'] = None
    invalid_payload['well'] = None

    invalid = _validate(invalid_payload, model_name='MicroCore')

    assert invalid.errors() is not None
    # Count errors and assert that there are three errors in concordance with
    # the number of invalid fields in the invalid_payload
    assert len(invalid.errors()) == 3

# TEST VIEWS


@pytest.mark.django_db
def test_microcore_get_form(auth_client, user, well):
    '''
    AC: Authenticated user is required
    AC: Should be bounded to a well automatically
    AC: get request has to take a well name
    AC: User needs to be authenticated to access this view
    '''
    # Check that the url link is setup correctly
    assert reverse("microcores", kwargs={
                   'pk': well.pk}) == f"/wells/{well.pk}/microcores/create/"

    # Check that the view is only accessible to authenticated users
    response = auth_client.get(reverse("microcores", kwargs={'pk': well.pk}))
    assert response.status_code == 302
    assert response.url == "/accounts/login/"

    auth_client.force_login(user)
    response = auth_client.get(reverse("microcores", kwargs={'pk': well.pk}))

    assert response.status_code == 200

@pytest.mark.django_db
def test_microcore_post_form(auth_client, user, well, microcore_json, invalid_microcore_json):
    '''
    AC: Authenticated user is required
    AC: url query must have the well pk    
    AC: Submission redirects to the well core list
    AC: Invalid submission redirects to the same page and shows errors per field
    AC: Invalid submission also returns a message that the submission is invalid
    AC: Form needs to be validated with pyndantic before saving
    AC: The well name should be shortened
    '''
    # Just a rename for convenience
    valid_payload = microcore_json
    invalid_payload = invalid_microcore_json

    microcore_view = MicroCoreFormView()
    assert microcore_view is not None

    # Check that the url link is setup correctly
    # create a post request
    post_data = microcore_json
    
    post_url = reverse("microcores", kwargs={'pk': well.pk})
    
    # raises an error if user is not authenticated
    with pytest.raises(Exception):
        response = auth_client.post(post_url, post_data)
        assert response.status_code == 302
        assert response.url == "/accounts/login/"
    
    auth_client.force_login(user)

    # If form is invalid it should return the same page with errors
    response = auth_client.post(post_url, invalid_payload)
    assert response.status_code == 200
    assert response.context['form'].errors is not None

    # check for valid submission
    response = auth_client.post(post_url, valid_payload)
    assert response.context['form'].errors is None
    assert response.status_code == 302
    assert response.url == f"/wells/{well.pk}/microcores/"








