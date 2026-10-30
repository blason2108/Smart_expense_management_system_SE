import pytest

from accounts.models import User
from categories.models import Category


@pytest.fixture
def user(db):
    return User.objects.create_user("alice", "alice@example.test", "Reliable-Finance-2026!")


@pytest.fixture
def other(db):
    return User.objects.create_user("bob", "bob@example.test", "Reliable-Finance-2026!")


@pytest.fixture
def auth(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def category(user):
    return Category.objects.create(owner=user, name="Food", kind="expense")
