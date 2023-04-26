import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword'
    )
    return user


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
