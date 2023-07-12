import pytest
from django.test import Client
# import responses
from django.test import RequestFactory


@pytest.mark.django_db
def test_auth_client(auth_client, user):
    print(f"This is the auth_client: {auth_client.__dict__}")
    # Check client type
    print(f"This is the auth_client type: {type(auth_client)}")
    assert isinstance(auth_client, Client)

    # make a request
    response = auth_client.get('/cores/')
    response.wsgi_request.user = user
    assert response.wsgi_request.user == user 
