import pytest

from django.urls import reverse
from django.test import RequestFactory
from django.test import Client
from crudapp.models import Well
from crudapp.forms import WellForm
from crudapp.views import WellFormView

@pytest.fixture
def client():
    return Client()

# TEST WELL MODELS
@pytest.mark.django_db
def test_well_creation(well):
    assert well.name == "Test Well"


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
    form_data = {'name': 'New Well'}
    request = RequestFactory().post(reverse('wells'), data=form_data)
    response = view(request)

    assert response.status_code == 302  # Redirect to success_url
    assert Well.objects.filter(name=form_data['name']).exists()

    # Test invalid form submission
    existing_well = Well.objects.first()
    form_data = {'name': existing_well.name}
    request = RequestFactory().post(reverse('wells'), data=form_data)
    response = view(request)
    assert response.status_code == 200
    assert not response.context_data['form'].is_valid()
    
