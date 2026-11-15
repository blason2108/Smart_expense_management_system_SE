import pytest
from django.test import Client, override_settings
from django.urls import reverse

from accounts.models import User
from audit.models import AuditEvent

pytestmark = pytest.mark.django_db


def registration(**changes):
    return dict(
        username="newuser",
        email="New@Example.test",
        password1="New-Strong-Phrase-2026!",
        password2="New-Strong-Phrase-2026!",
        **changes,
    )


def test_registration(client):
    r = client.post("/accounts/register/", registration())
    assert r.status_code == 302
    u = User.objects.get(username="newuser")
    assert u.email == "new@example.test"
    assert u.check_password("New-Strong-Phrase-2026!")


@pytest.mark.parametrize(
    "change",
    [
        {"email": "alice@example.test"},
        {"email": "ALICE@EXAMPLE.TEST"},
        {"username": "alice"},
        {"email": "invalid"},
        {"password1": "123", "password2": "123"},
        {"password2": "different"},
        {"username": ""},
        {"password1": "1234567890", "password2": "1234567890"},
    ],
)
def test_invalid_registration(client, user, change):
    data = registration()
    data.update(change)
    assert client.post("/accounts/register/", data).status_code == 200
    assert User.objects.count() == 1


def test_registration_get(client):
    assert client.get("/accounts/register/").status_code == 200


def test_login_logout(client, user):
    assert (
        client.post("/accounts/login/", {"username": user.username, "password": "Reliable-Finance-2026!"}).status_code
        == 302
    )
    assert AuditEvent.objects.filter(actor=user, event="login").exists()
    assert client.get("/accounts/logout/").status_code == 405
    assert client.post("/accounts/logout/").status_code == 302
    assert AuditEvent.objects.filter(actor=user, event="logout").exists()


def test_failed_login_has_no_credentials(client, user, caplog):
    marker = "Highly-Secret-Wrong-Password!"
    r = client.post("/accounts/login/", {"username": user.username, "password": marker})
    assert r.status_code == 200
    entry = AuditEvent.objects.get(event="login_failed")
    assert entry.actor is None
    assert marker not in caplog.text
    assert marker not in str(entry.__dict__)


@pytest.mark.parametrize("path", ["/", "/categories/", "/transactions/", "/budgets/", "/reports/"])
def test_protected(client, path):
    assert client.get(path).status_code == 302


def test_admin_denies_standard_user(auth):
    assert auth.get("/django-admin/accounts/user/").status_code == 302


def test_admin_users_and_audit(client, user):
    user.is_staff = user.is_superuser = True
    user.save()
    client.force_login(user)
    assert client.get("/django-admin/accounts/user/").status_code == 200
    assert client.get("/django-admin/audit/auditevent/").status_code == 200


def test_admin_deactivation_and_audit(client, user, other):
    change_url = reverse("admin:accounts_user_change", args=[other.pk])
    other.email = "private-admin-change@example.test"
    form_data = {
        "username": other.username,
        "email": other.email,
        "date_joined_0": other.date_joined.date().isoformat(),
        "date_joined_1": "12:00:00",
        "_save": "Save",
    }

    client.force_login(user)
    assert client.post(change_url, form_data).status_code == 302
    assert User.objects.get(pk=other.pk).is_active
    assert not AuditEvent.objects.filter(event="admin_user_changed").exists()

    user.is_staff = user.is_superuser = True
    user.save()
    assert client.post(change_url, form_data).status_code == 302
    other.refresh_from_db()
    assert not other.is_active
    event = AuditEvent.objects.get(event="admin_user_changed", actor=user)
    assert event.timestamp
    audit_page = client.get(reverse("admin:audit_auditevent_changelist")).content
    assert b"admin_user_changed" in audit_page
    assert other.email.encode() not in audit_page
    assert other.password.encode() not in audit_page
    assert not Client().login(username=other.username, password="Reliable-Finance-2026!")


def test_csrf(user):
    c = Client(enforce_csrf_checks=True)
    c.force_login(user)
    assert c.post("/categories/new/", {"name": "No token", "kind": "expense"}).status_code == 403


@override_settings(
    SECURE_SSL_REDIRECT=True, SECURE_HSTS_SECONDS=31536000, SESSION_COOKIE_SECURE=True, CSRF_COOKIE_SECURE=True
)
def test_https(client):
    r = client.get("/healthz/")
    assert r.status_code == 301 and r.url.startswith("https://")
    secure = client.get("/healthz/", secure=True)
    assert secure.status_code == 200
    assert "31536000" in secure.headers["Strict-Transport-Security"]
