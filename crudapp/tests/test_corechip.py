import copy
from pprint import pprint as pp

import pytest

from crudapp.models import CoreChip
from crudapp.views import _validate , CoreChipFormView
from datamodel import CoreChip as CorechipModel

from django.urls import reverse
from django.test import Client
from django.db import IntegrityError


@pytest.fixture
def corechip(well, user, core):
    # Shorten the name as it is required for the corechip name
    well_name_short = well.gen_short_name()

    return CoreChip.objects.create(
        well=well,
        registration_date='2021-06-22 13:00:00',
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
    return {
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

print('Corechip JSON:', corechip_json)

# TEST MODEL
@pytest.mark.django_db
def test_create_corechip(corechip_json, user, well):
    # Check that the corechip was createed
    assert CoreChip.objects.count() == 1

    retrieved_corechip = CoreChip.objects.first()
    assert retrieved_corechip.corechip_name == corechip_json['corechip_name']

    # deepcopy the corechip_json
    duplicate_corechip = copy.deepcopy(corechip_json)

    # Replace those fields that require actual objects
    duplicate_corechip['well'] = well
    duplicate_corechip['registered_by'] = user

    # drop well_name and core_type 
    duplicate_corechip.pop('well_name')
    duplicate_corechip.pop('core_type')

    with pytest.raises(IntegrityError):
        # Recreate a corechip instance by copypasting corechip
        # This should raise an error because corechip_name is unique
        CoreChip.objects.create(**duplicate_corechip)
    

def test_update_corechip():
    ''' Here we have new optional data to be added
    '''


    # We raise an error if user tries to change the name of the corechip
    pass

def test_delete_corechip():
    pass

# TEST VALIDATION
@pytest.mark.django_db
def test_validate_corechip(corechip_json):
    ''' 
    input: a post request with a corechip
    process: pydantic model vaidates the corechip
    output: validation result
    '''

    corechip_view = CoreChipFormView()
    _validate(corechip_json, model_name='CoreChip')     
        
    # Make a copy of corechip data to make it invalid
    corechip_json_copy = copy.deepcopy(corechip_json)
    
    # Alter the corechip data to make it invalid
    corechip_json_copy['corechip_name'] = None
    invalid = _validate(corechip_json_copy, model_name='CoreChip')
    assert invalid.errors() is not None


# TEST VIEWS
# This is business logic
def test_create_corechip_view():
    pass

def test_update_corechip_view():
    
    # We raise an error if user tries to change the name of the corechip
    # The error can be simply a dialog box that says "You cannot change the name of a corechip"
    # And it can suggest that the user deletes, or archives the corechip and creates a new one
    pass

def test_delete_corechip_view():
    pass

# TEST FORMS
@pytest.mark.django_db
def test_corechip_form_view_get_initial(well, request_factory):
    view = CoreChipFormView()

    # Test that a wel with id 1 exists
    assert well.name == 'Test Well'
    
    # The request url should be this one:/wells/1/cores/create/?well_name=DAP&core_number=C1
    # Build request so that it resembles the one above
    url = reverse('corechips', kwargs={'pk': well.id })

    request = request_factory.get(url)
    view.request = request

    view.kwargs = {'pk': well.pk, 'well_name': well.name, 'core_number': 'C1'}  
    initial = view.get_initial()

    assert 'collection_date' in initial
    assert 'well_name' in initial

@pytest.mark.django_db
def test_corechip_get_form(well, auth_client, user, core):
    ''' Here we test that the form is returned correctly as a resource in the response
    '''
    
    # Build url for the corechip form
    url = reverse('corechips', kwargs={'pk': well.id})
    assert url is not None
    assert url == f'/wells/{well.id}/corechips/create/'

    # Create request content
    data = {
        'well_name': well.name,
        'core_number': core.core_number,
        'core_section_name': core.core_section_name,
        'core_section_number': core.core_number,
    }

    auth_client.force_login(user)
    response = auth_client.get(url, data=data)

    assert response.status_code == 200

    # Check the response body
    assert response.context['form'] is not None
    assert response.context['core_number'] == core.core_number 

@pytest.mark.django_db
def test_corechip_get(well, core, auth_client, user):
    # Now we check that initial values are set correctly
    auth_client.force_login(user)
    response = auth_client.get(reverse("corechips", kwargs={'pk': well.pk}), data={
        'well_pk': well.id, # This is the well id
        'well_name': well.name,
        'core_number': core.core_number,
        'core_section_name': core.core_section_name,
    })

    initial = response.context['form'].initial

    assert initial['well_pk'] == str(well.id)
    assert initial['well_name'] == well.name
    assert initial['core_section_name'] == core.core_section_name
    assert initial['core_number'] == core.core_number

    assert response.status_code == 200

@pytest.mark.django_db
def test_corechip_post_request(auth_client, corechip_json, user, well, core):
    ''' 
    '''
    assert CorechipModel is not None

    data = copy.deepcopy(corechip_json) # the data to be posted
    # change corechip name
    data['corechip_name'] = well.gen_short_name() + '-C1-2-CHB8' # 8 instead of 7 because 7 already exists and adding new corechips should be sequencial

    auth_client.force_login(user)

    response = auth_client.get(reverse("corechips", kwargs={'pk': well.pk}), data=data)

    post_request_url= reverse('corechips', kwargs={'pk': well.pk})

    post_request_url += '?' + '&'.join([f'{key}={value}' for key, value in data.items()])

    # Make a post request to create a corechip
    response = auth_client.post(post_request_url, data=data)

    assert response.status_code == 302
    assert CoreChip.objects.filter(corechip_name=data['corechip_name']).exists()
    assert response.url == f"/wells/{well.pk}/samples/create/"


def test_corechip_form_view_from_core_list():
    '''
    AC: Each core allows to add a corechip, when the user clicks on the add corechip button, the corechip form view is displayed
    '''
    pass