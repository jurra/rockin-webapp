import pytest

from django.urls import reverse
from django.test import RequestFactory
from django.test import Client
# from mixer.backend.django import mixer
from crudapp.models import Well
from crudapp.forms import WellForm
from crudapp.views import WellFormView

'''
In these tests, we're using the Client object provided by Django to simulate HTTP requests to our view. We're also using the mixer library to create sample data for our tests.
The first test test_well_form_view_get checks that the view returns a valid response when accessed with an HTTP GET request.
The second test test_well_form_view_post_existing_well checks that the view correctly handles a form submission with a well name that already exists in the database and returns a validation error on the well_name field.
The third test test_well_form_view_post_new_well checks that the view correctly handles a form submission with a new well name and saves it to the database, redirecting to the core_list view as expected.
'''


@pytest.fixture
def client():
    return Client()

# TEST WELL MODELS
@pytest.mark.django_db
def test_well_creation(well):
    assert well.well_name == "Test Well"


# TEST WELL VIEWS
@pytest.mark.django_db
def test_well_form_view():
    request = RequestFactory().get(reverse('wells'))
    view = WellFormView.as_view()
    response = view(request)

    # Test that the template used by the view is correct
    assert response.template_name == ['core.html']

    # Test that the form used by the view is correct
    assert isinstance(response.context_data['form'], WellForm)

    # Test valid form submission
    form_data = {'well_name': 'New Well'}
    request = RequestFactory().post(reverse('wells'), data=form_data)
    response = view(request)
    assert response.status_code == 302  # Redirect to success_url
    assert Well.objects.filter(well_name=form_data['well_name']).exists()

    # Test invalid form submission
    existing_well = Well.objects.first()
    form_data = {'well_name': existing_well.well_name}
    request = RequestFactory().post(reverse('wells'), data=form_data)
    response = view(request)
    assert response.status_code == 200
    assert not response.context_data['form'].is_valid()
    
    ## Something like what's bellow could be done but it would require to render the template
    ## otherwise it will give an error: E  django.template.response.ContentNotRenderedError: The response content must be rendered before it can be accessed.
    # assert 'This well already exists.' in response.content.decode('utf-8')
