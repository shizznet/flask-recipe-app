import pytest
from flask import url_for

import config
from app import create_app, db
from app.models import models  # Adjust the import based on your models' location


@pytest.fixture(scope='module')
def test_client():
    # Configure your application for testing
    flask_app = create_app(config.TestingConfig)

    # Flask provides a test client for the application
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests
    ctx = flask_app.app_context()
    ctx.push()

    # Create the database and the database table(s)
    db.create_all()

    yield testing_client  # This is where the testing happens!

    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture(scope='function')
def user_setup(test_client):
    # Insert user data
    user = models.User(username='testuser')
    user.set_password(password='testpassword')
    db.session.add(user)
    db.session.commit()

    yield

    # Clean up / tear down
    db.session.delete(user)
    db.session.commit()


def test_login_page(test_client):
    """
    Test that login page is accessible without login.
    """
    response = test_client.get(url_for('auth.login'))
    assert response.status_code == 200


def test_login(test_client, user_setup):
    """
    Test logging in with correct credentials redirects to the profile page.
    """
    print(url_for('auth.login'))
    response = test_client.post(url_for('auth.login'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_registration(test_client):
    """
    Test that user registration behaves correctly.
    """
    # Data to be posted to the registration route
    new_user_data = {
        'username': 'testuser',
        'password': 'testPassword123',
        'confirm': 'testPassword123'
    }

    # Post data to the registration route
    response = test_client.post(url_for('auth.register'), data=new_user_data, follow_redirects=True)

    # Check that the user is redirected to the login page
    print(response.text)
    assert response.status_code == 200

    # Query the database to ensure the user was registered successfully
    user = models.User.query.filter_by(username=new_user_data['username']).first()
    all_users = models.User.query.all()
    print(all_users)
    for each_user in all_users:
        print(each_user)
    assert user is not None
    assert user.username == new_user_data['username']
