import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_password_is_hashed():  # TC-SEC-01
    user = get_user_model().objects.create_user("u1", "u1@example.com", "S3cure-pass!")
    assert user.password != "S3cure-pass!"
    assert user.password.startswith("pbkdf2_sha256$")


@pytest.mark.django_db
def test_duplicate_email_rejected():  # TC-AUTH-01 (model level)
    from django.db import IntegrityError
    User = get_user_model()
    User.objects.create_user("a", "same@example.com", "S3cure-pass!")
    with pytest.raises(IntegrityError):
        User.objects.create_user("b", "same@example.com", "S3cure-pass!")


def test_health_endpoint(client):
    assert client.get(reverse("dashboard:health")).json() == {"status": "ok"}


@pytest.mark.django_db
def test_dashboard_requires_login(client):  # TC-SEC-02 (smoke)
    resp = client.get(reverse("dashboard:home"))
    assert resp.status_code == 302 and "/accounts/login/" in resp.url
