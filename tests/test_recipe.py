from contextlib import contextmanager

import pytest
from flask import template_rendered, url_for

import config
from app import create_app, db
from app.models import models


@pytest.fixture(scope="module")
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

    # Create a user for testing
    test_user = models.User(username="testuser1")
    test_user.set_password("testpassword1")
    db.session.add(test_user)
    db.session.commit()

    testing_client.post(
        url_for(config.AUTH_LOGIN),
        data={"username": "testuser1", "password": "testpassword1"},
        follow_redirects=True,
    )

    yield testing_client

    # Cleanup: remove user and tables, then logout
    db.session.delete(test_user)
    db.session.remove()
    db.drop_all()
    ctx.pop()


@contextmanager
def captured_templates(app):
    """Capture templates rendered during request handling."""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def test_add_recipe(test_client):
    with captured_templates(test_client.application) as templates:
        response = test_client.post(
            url_for("recipe.add_recipe"),
            data={
                "title": "test title",
                "description": "test description",
                "instructions": "test instruction",
                "ingredients-0-title": "test ingredient",
                "ingredients-0-quantity": "10",
                "ingredients-0-measurement_type": "grams",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == "recipes.html"
        assert len(context["recipes"]) == 1
        assert any(r.title == "test title" for r in context["recipes"])

        assert "test title" in response.get_data(as_text=True)
        assert "test description" in response.get_data(as_text=True)


def test_list_recipes(test_client):
    with captured_templates(test_client.application) as templates:
        response = test_client.get(url_for(config.VIEW_RECIPES))

        assert response.status_code == 200

        assert len(templates) == 1

        template, context = templates[0]
        assert template.name == "recipes.html"
        assert len(context["recipes"]) == 1
        assert any(r.title == "test title" for r in context["recipes"])

        assert "test title" in response.get_data(as_text=True)
        assert "test description" in response.get_data(as_text=True)


def test_view_recipe(test_client):
    with captured_templates(test_client.application) as templates:
        response = test_client.get(url_for("recipe.view_recipe", id=1))

        assert response.status_code == 200

        assert len(templates) == 1

        template, context = templates[0]
        assert template.name == "recipe_view.html"
        assert context["recipe"].title == "test title"
        assert context["recipe"].description == "test description"
        assert context["recipe"].instructions == "test instruction"

        for ingredient in context["recipe"].ingredients:
            assert ingredient.title == "test ingredient"
            assert ingredient.quantity == "10"
            assert ingredient.measurement_type == "grams"

        assert "test title" in response.get_data(as_text=True)
        assert "test description" in response.get_data(as_text=True)
        assert "test instruction" in response.get_data(as_text=True)
        assert "test ingredient" in response.get_data(as_text=True)
        assert "10 grams" in response.get_data(as_text=True)


def test_edit_recipe(test_client):
    with captured_templates(test_client.application) as templates:
        response = test_client.post(
            url_for("recipe.edit_recipe", id=1),
            data={
                "title": "test title1",
                "description": "test description1",
                "ingredients-0-title": "test ingredient1",
                "ingredients-0-quantity": "10",
                "ingredients-0-measurement_type": "grams",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == "recipes.html"
        assert len(context["recipes"]) == 1
        assert any(r.title == "test title1" for r in context["recipes"])

        for ingredient in context["recipes"][0].ingredients:
            assert ingredient.title == "test ingredient1"
            assert ingredient.quantity == "10"
            assert ingredient.measurement_type == "grams"

        assert "test title1" in response.get_data(as_text=True)
        assert "test description1" in response.get_data(as_text=True)
