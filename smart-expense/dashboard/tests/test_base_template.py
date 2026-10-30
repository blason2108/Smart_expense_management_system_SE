import pytest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.urls import reverse


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user("u1", "u1@example.com", "S3cure-pass!")


@pytest.mark.django_db
def test_nav_for_anonymous_has_login_only(client):  # TC-UX-01 (navigation)
    html = client.get(reverse("accounts:login")).content.decode()
    assert '<nav class="navbar"' in html
    assert 'href="/accounts/login/"' in html
    assert "Logout" not in html


@pytest.mark.django_db
def test_nav_for_authenticated_has_dashboard_and_logout(client, user):  # TC-UX-01
    client.force_login(user)
    html = client.get(reverse("dashboard:home")).content.decode()
    assert "Dashboard" in html and "Logout" in html
    assert 'aria-current="page"' in html  # active link is marked


@pytest.mark.django_db
def test_invalid_login_shows_clear_validation_message(client, user):  # TC-UX-01 (validation messaging)
    resp = client.post(reverse("accounts:login"), {"username": "u1", "password": "wrong"})
    html = resp.content.decode()
    assert resp.status_code == 200
    assert 'class="alert alert-error"' in html and 'role="alert"' in html


@pytest.mark.django_db
def test_empty_login_shows_field_errors(client):  # TC-UX-01
    html = client.post(reverse("accounts:login"), {}).content.decode()
    assert html.count('class="field-error"') == 2
    assert "has-error" in html


def test_messages_partial_maps_levels_to_css_classes():
    request = RequestFactory().get("/")
    request.session = {}
    request._messages = FallbackStorage(request)
    messages.success(request, "Saved")
    messages.error(request, "Broken")
    html = render_to_string("partials/messages.html", {"messages": messages.get_messages(request)})
    assert "alert-success" in html and "alert-error" in html
    assert 'role="status"' in html and 'role="alert"' in html
