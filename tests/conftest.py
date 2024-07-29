import pytest
from flask import url_for
from project_real_estate import app
from project_real_estate.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture
def init_database():
    # Mocked data for tests, replace with appropriate setup if needed
    admin_user = User(id=1, username='admin', email='admin@example.com', is_admin=True)
    regular_user = User(id=2, username='user', email='user@example.com', is_admin=False)

    return {
        "admin": admin_user,
        "user": regular_user,
        "properties": []  # Add mock properties here if needed
    }

@pytest.fixture
def login_admin_user(test_client, init_database):
    test_client.post('/login', data=dict(
        email=init_database['admin'].email,
        password='admin_password'
    ), follow_redirects=True)
    yield
    test_client.get('/logout', follow_redirects=True)

@pytest.fixture
def login_regular_user(test_client, init_database):
    test_client.post('/login', data=dict(
        email=init_database['user'].email,
        password='user_password'
    ), follow_redirects=True)
    yield
    test_client.get('/logout', follow_redirects=True)
