from decimal import Decimal
from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError

from categories.models import Category
from transactions.models import Transaction


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
def test_seed_creates_categories_and_transactions_for_standard_user():
    out = run("--force")
    std = get_user_model().objects.get(username="user1")
    assert "Seed data complete." in out
    assert Category.objects.filter(owner=std, kind=Category.INCOME).count() == 2
    assert Category.objects.filter(owner=std, kind=Category.EXPENSE).count() == 7
    txns = Transaction.objects.filter(owner=std)
    assert txns.count() == 7
    # Every transaction's type matches its category's type and amounts are positive.
    assert all(t.kind == t.category.kind and t.amount > 0 for t in txns)
    assert txns.get(description="Groceries").amount == Decimal("850.50")
    # The admin account is only for administration: it owns no financial data.
    assert not Category.objects.filter(owner__username="admin1").exists()


@pytest.mark.django_db
def test_seed_is_idempotent():
    run("--force")
    run("--force")
    assert get_user_model().objects.filter(username__in=["user1", "admin1"]).count() == 2
    assert Category.objects.count() == 9
    assert Transaction.objects.count() == 7


@pytest.mark.django_db
def test_seed_does_not_duplicate_when_rerun_on_a_later_day(monkeypatch):
    import datetime

    import accounts.management.commands.seed_data as seed

    run("--force")

    class LaterDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date.today() + datetime.timedelta(days=3)

    monkeypatch.setattr(seed, "date", LaterDate)
    run("--force")
    assert Transaction.objects.count() == 7


@pytest.mark.django_db
def test_seed_reuses_existing_category_with_different_case():
    std = get_user_model().objects.create_user("user1", "user1@example.com", "x")
    Category.objects.create(owner=std, name="food", kind=Category.EXPENSE)
    run("--force")
    assert Category.objects.filter(owner=std, name__iexact="food").count() == 1


@pytest.mark.django_db
def test_seed_uses_env_passwords(monkeypatch):
    monkeypatch.setenv("SEED_USER_PASSWORD", "Custom#9999")
    run("--force")
    assert get_user_model().objects.get(username="user1").check_password("Custom#9999")


@pytest.mark.django_db
def test_seed_reset_restores_passwords():
    run("--force")
    std = get_user_model().objects.get(username="user1")
    std.set_password("changed")
    std.save()
    run("--force")
    assert not get_user_model().objects.get(username="user1").check_password("User#12345")
    run("--force", "--reset")
    assert get_user_model().objects.get(username="user1").check_password("User#12345")


@pytest.mark.django_db
def test_seed_refuses_without_debug_or_force(settings):
    settings.DEBUG = False
    with pytest.raises(CommandError):
        run()
    assert not get_user_model().objects.exists()


@pytest.mark.django_db
def test_seed_runs_without_force_when_debug_is_on(settings):
    settings.DEBUG = True
    assert "Seed data complete." in run()
