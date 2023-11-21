import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_create_sample(well):
    '''
    WHEN user clicks on well, THEN user is redirected to well detail page, THEN the user can create a sample
    WHEN user clicks on create sample, THEN user is redirected to create sample page
    '''

    # Assert that a link triggers a view response in this case the SampleFormView
    assert reverse("create_sample", kwargs={'pk': well.pk}) == f"/wells/{well.pk}/samples/create/"