import copy
from pprint import pprint

import pytest
from pydantic import ValidationError
from django.test import RequestFactory

from crudapp.models import CoreChip
from crudapp.views import _validate , CoreChipFormView
from datamodel import CoreChip as CorechipModel

from django.urls import reverse
from django.test import Client

@pytest.fixture
def corechip_post_request(user, well):
    client = Client()
    client.force_login(user)

    # Data for the corechip post request
    corechip_data = {
        'core_id': 1,
        'core_chip_number': 1,
        'from_top_bottom': 'Top',
        'core_chip_name': 'Test Chip',
        'core_chip_depth': 10.5,
        'lithology': 'Test Lithology',
        'remarks': 'Test Remarks',
        'debris': True,
        'formation': 'Test Formation',
    }

    # Make a post request to create a corechip
    well_id = well.id
    url = reverse('well_core_list', args=[well_id])  # Replace 'corechip_create' with the actual URL name of the view for corechip creation
    response = client.post(url, data=corechip_data)

    return response

# TEST MODEL
@pytest.mark.django_db
def test_create_corechip(corechip_data):
    # Check that the corechip was createed
    print(corechip_data)
    assert CoreChip.objects.count() == 1

    retrieved_corechip = CoreChip.objects.first()
    assert retrieved_corechip.corechip_name == corechip_data['corechip_name']

def test_update_corechip():
    ''' Here we have new optional data to be added
    '''


    # We raise an error if user tries to change the name of the corechip
    pass

def test_delete_corechip():
    pass

# TEST VALIDATION
@pytest.mark.django_db
def test_validate_corechip(corechip_data, corechip_post_request):
    ''' 
    input: a post request with a corechip
    process: pydantic model vaidates the corechip
    output: validation result
    '''
    assert CorechipModel is not None

    corechip_view = CoreChipFormView()
    _validate(corechip_view, corechip_data, model_name='CoreChip')
    # TODO: _validate(corechip_view, corechip_post_request, model_name='CoreChip')
     
        
    # Make a copy of corechip data  
    corechip_data_copy = copy.deepcopy(corechip_data)
    
    # Alter the corechip data to make it invalid
    corechip_data_copy['corechip_name'] = ''
    invalid = _validate(corechip_view, corechip_data_copy, model_name='CoreChip')
    assert invalid.errors() is not None

def test_reject_duplicate_corechip():
    pass


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
    assert well.id == 1
    assert well.name == 'Test Well'
    
    # The request url should be this one:/wells/1/cores/create/?well_name=DAP&core_number=C1
    # Build request so that it resembles the one above
    url = reverse('corechips', kwargs={'pk': well.id })

    request = request_factory.get(url)
    view.request = request

    view.kwargs = {'pk': well.pk, 'well_name': well.name, 'core_number': 'C1'}  
    initial = view.get_initial()

    assert 'collection_date' in initial
    assert 'well' in initial
    assert 'core_section_name' in initial
    initial['core_section_name'] is not None
    print(initial)

@pytest.mark.django_db
def test_corechip_get_form(well, auth_client, user, core):
    ''' Here we test that the form is returned correctly as a resource in the response
    '''
    
    # Build url for the corechip form
    url = reverse('corechips', kwargs={'pk': 1})
    assert url is not None
    assert url == '/wells/1/corechips/create/'


    # Create request content
    data = {
        'well_name': well.name,
        'core_number': core.core_number,
        'core_section_name': core.core_section_name,
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

    debug = response.context['DEBUG']
    assert debug is not None
    assert debug['well_name'] is not None
    print(debug)

@pytest.mark.django_db
def test_corechip_post_request(auth_client, corechip_data, user, well, core):
    ''' 
    input: a post request with a corechip
    process: pydantic model vaidates the corechip
    output: validation result
    '''
    assert CorechipModel is not None

    auth_client.force_login(user)

    response = auth_client.get(reverse("corechips", kwargs={'pk': well.pk}), data={
        'well_pk': well.id, # This is the well id
        'well_name': well.name,
        'core_number': core.core_number,
        'core_section_name': core.core_section_name,
    })

    initial = response.context['form'].initial

    data = copy.deepcopy(corechip_data)

    corechip_view = CoreChipFormView()
    valid = _validate(corechip_view, data, model_name='CoreChip')

    # add data in initial to data   
    data.update(initial)

    # Make a post request to create a corechip
    response = auth_client.post(reverse('corechips', kwargs={'pk': well.pk}), data=data)

    assert response.status_code == 302
    assert CoreChip.objects.filter(corechip_name=data['corechip_name']).exists()

def test_corechip_form_view_from_core_list():
    '''
    AC: Each core allows to add a corechip, when the user clicks on the add corechip button, the corechip form view is displayed
    '''
    pass