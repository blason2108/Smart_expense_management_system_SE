from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError


def run(*args):
    out = StringIO()
    call_command("seed_data", *args, stdout=out)
    return out.getvalue()


@pytest.mark.django_db
def test_seed_creates_standard_and_admin_users():
    run("--force")
    User = get_user_model()
    std, adm = User.objects.get(username="user1"), User.objects.get(username="admin1")
    assert not std.is_staff and not std.is_superuser
    assert adm.is_staff and adm.is_superuser
    assert std.check_password("User#12345") and adm.check_password("Admin#12345")


@pytest.mark.django_db
def test_seed_is_idempotent():
    run("--force")
    run("--force")
    assert get_user_model().objects.filter(username__in=["user1", "admin1"]).count() == 2


@pytest.mark.django_db
def test_seed_uses_env_passwords(monkeypatch):
    monkeypatch.setenv("SEED_USER_PASSWORD", "Custom#9999")
    run("--force")
    assert get_user_model().objects.get(username="user1").check_password("Custom#9999")


@pytest.mark.django_db
def test_seed_refuses_without_debug_or_force():
    with pytest.raises(CommandError):
        run()


@pytest.mark.django_db
def test_seed_skips_missing_models_without_crashing():
    # Category/Transaction models are built in other issues; the command must not fail meanwhile.
    out = run("--force")
    assert "Seed data complete." in out
