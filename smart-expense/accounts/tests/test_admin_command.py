import io

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("email", ["alice@example.test", "ALICE@EXAMPLE.TEST"])
def test_admin_command_rejects_existing_email_without_traceback(user, email):
    with pytest.raises(CommandError, match="email is already registered"):
        call_command("create_demo_admin", username="se_admin", email=email, interactive=False, stdout=io.StringIO())
    assert not get_user_model().objects.filter(username="se_admin").exists()
    user.refresh_from_db()
    assert not user.is_staff and not user.is_superuser


def test_admin_command_creates_separate_administrator(user, monkeypatch):
    monkeypatch.setenv("DJANGO_SUPERUSER_PASSWORD", "Disposable-Admin-2026!")
    call_command(
        "create_demo_admin", username="se_admin", email="se-admin@example.test", interactive=False, stdout=io.StringIO()
    )
    admin = get_user_model().objects.get(username="se_admin")
    assert admin.is_active and admin.is_staff and admin.is_superuser
    assert admin.check_password("Disposable-Admin-2026!")
    user.refresh_from_db()
    assert not user.is_staff and not user.is_superuser
