import pytest

from django.db import connection
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import RequestFactory
from crudapp.models import Well
from crudapp.forms import WellForm
from crudapp.views import WellFormView


# Test that the well fixture exists in the database
@pytest.mark.django_db
def test_well_fixture(well):
    assert Well.objects.count() == 1
    assert Well.objects.first().name == well.name
    assert Well.objects.first().id == 1

    # Double check that the fixture exists in the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM crudapp_well")
        assert cursor.fetchone()[0] == well.name
        cursor.execute("SELECT id FROM crudapp_well")
        assert cursor.fetchone()[0] == 1

# TEST WELL MODELS
@pytest.mark.django_db
def test_well_creation(well):
    assert well.name == "Test Well"

@pytest.mark.django_db
def test_reject_duplicate_well():
    # Set up test data
    Well.objects.create(name='Well 1')

    with pytest.raises(IntegrityError):
        Well.objects.create(name='Well 1')

@pytest.mark.django_db
def test_reject_empty_well():
    with pytest.raises(ValidationError):
        Well.objects.create(name='')

@pytest.mark.django_db
def test_well_short_name(well):
    well.name = 'DEL-GT-01'
    well_alias = well.gen_short_name()
    assert well_alias == 'DELGT01'
    well.name = 'DEL GT 01'
    well_alias = well.gen_short_name()
    assert well_alias == 'DELGT01'


# TEST WELL VIEWS
@pytest.mark.django_db
def test_well_list_view(auth_client, user):
    # Set up test data
    Well.objects.create(name='Well 1')
    Well.objects.create(name='Well 2')

    auth_client.force_login(user)

    # Send a GET request to the well_list URL
    response = auth_client.get(reverse('well_list'))

    # Assert that the response has a status code of 200 (OK)
    assert response.status_code == 200

    # Assert that the 'well_list' context variable exists in the response
    assert 'wells' in response.context

    # Assert that the 'well_list' context variable contains the expected wells
    well_list = response.context['wells']
    assert well_list.count() == 2
    assert [well.name for well in well_list] == ['Well 1', 'Well 2']

@pytest.mark.django_db
def test_well_form_view():
    request = RequestFactory().get(reverse('well_list'))
    view = WellFormView.as_view()
    response = view(request)

    # Test that the template used by the view is correct
    assert response.template_name == ['well.html']

    # Test that the form used by the view is correct
    assert isinstance(response.context_data['form'], WellForm)

    # Test valid form submission
    form_data = {'name': 'New Well'}
    request = RequestFactory().post(reverse('well_list'), data=form_data)
    response = view(request)

    assert response.status_code == 302  # Redirect to success_url
    assert Well.objects.filter(name=form_data['name']).exists()

    # Test invalid form submission
    existing_well = Well.objects.first()
    form_data = {'name': existing_well.name}
    request = RequestFactory().post(reverse('well_list'), data=form_data)
    response = view(request)
    assert response.status_code == 200
    assert not response.context_data['form'].is_valid()

@pytest.mark.django_db
def test_well_form_view_reject_duplicate():
    assert 1 == 2