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


@pytest.mark.django_db
def test_nav_for_anonymous_also_offers_register(client):  # TC-UX-01
    html = client.get(reverse("accounts:login")).content.decode()
    assert reverse("accounts:register") in html
    for protected in ("categories:list", "transactions:list", "budgets:list", "reports:list"):
        assert reverse(protected) not in html


@pytest.mark.django_db
def test_nav_links_every_feature_page_for_authenticated_user(client, user):  # TC-UX-01
    client.force_login(user)
    html = client.get(reverse("dashboard:home")).content.decode()
    for name in ("dashboard:home", "categories:list", "transactions:list", "budgets:list", "reports:list"):
        assert f'href="{reverse(name)}"' in html
    assert "/django-admin/" not in html  # staff-only link


@pytest.mark.django_db
def test_nav_shows_admin_link_for_staff_only(client, user):
    user.is_staff = True
    user.save()
    client.force_login(user)
    assert 'href="/django-admin/"' in client.get(reverse("dashboard:home")).content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("name", ["categories:list", "transactions:list", "budgets:list", "reports:list"])
def test_active_nav_link_follows_current_page(client, user, name):  # TC-UX-01
    client.force_login(user)
    html = client.get(reverse(name)).content.decode()
    assert html.count('aria-current="page"') == 1
    assert f'class="nav-link active" href="{reverse(name)}" aria-current="page"' in html


@pytest.mark.django_db
def test_base_template_keeps_dashboard_content(client, user):
    """Regression: the base-template work must not replace the real dashboard with a placeholder."""
    client.force_login(user)
    html = client.get(reverse("dashboard:home")).content.decode()
    assert "Your financial overview" in html and "Budget status and alerts" in html
    assert "placeholder" not in html


@pytest.mark.django_db
def test_pages_link_the_shared_stylesheet(client):
    assert "css/app.css" in client.get(reverse("accounts:login")).content.decode()
