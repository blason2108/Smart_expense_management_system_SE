"""Seed demo/test data (FND-05): standard + admin users, predefined categories, sample transactions.

Usage:  python manage.py seed_data [--force] [--reset]

* Idempotent: running it repeatedly (even on different days) does not create duplicates.
* Refuses to run when DEBUG is False unless --force (the seeded passwords are well known).
* Passwords come from SEED_USER_PASSWORD / SEED_ADMIN_PASSWORD (dev defaults below).
* Categories and transactions belong to the standard user (``user1``): every Category/Transaction
  is owned by exactly one user in this app (``owner`` FK).
"""

import os
from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from categories.models import Category
from transactions.models import Transaction

STANDARD_USER = {"username": "user1", "email": "user1@example.com"}
ADMIN_USER = {"username": "admin1", "email": "admin1@example.com"}

PREDEFINED_CATEGORIES = [
    ("Salary", Category.INCOME),
    ("Freelance", Category.INCOME),
    ("Food", Category.EXPENSE),
    ("Transport", Category.EXPENSE),
    ("Rent", Category.EXPENSE),
    ("Utilities", Category.EXPENSE),
    ("Entertainment", Category.EXPENSE),
    ("Health", Category.EXPENSE),
    ("Shopping", Category.EXPENSE),
]

# (days_ago, category name, amount, description). The kind is taken from the category.
SAMPLE_TRANSACTIONS = [
    (28, "Salary", "50000.00", "Monthly salary"),
    (25, "Rent", "15000.00", "Monthly rent"),
    (20, "Food", "850.50", "Groceries"),
    (14, "Transport", "400.00", "Metro card top-up"),
    (9, "Utilities", "1200.00", "Electricity bill"),
    (5, "Entertainment", "600.00", "Movie night"),
    (2, "Food", "320.00", "Lunch"),
]


class Command(BaseCommand):
    help = "Seed standard + admin users, predefined categories and sample transactions."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Allow running when DEBUG is False.")
        parser.add_argument("--reset", action="store_true", help="Reset seeded users' passwords.")

    @transaction.atomic
    def handle(self, *args, **opts):
        if not settings.DEBUG and not opts["force"]:
            raise CommandError("Refusing to seed with DEBUG=False. Use --force if you really mean it.")
        user = self._seed_user(STANDARD_USER, os.environ.get("SEED_USER_PASSWORD", "User#12345"), opts["reset"])
        self._seed_user(ADMIN_USER, os.environ.get("SEED_ADMIN_PASSWORD", "Admin#12345"), opts["reset"], admin=True)
        categories = self._seed_categories(user)
        self._seed_transactions(user, categories)
        self.stdout.write(self.style.SUCCESS("Seed data complete."))

    def _seed_user(self, data, password, reset, admin=False):
        obj, created = get_user_model().objects.get_or_create(
            username=data["username"],
            defaults={"email": data["email"], "is_staff": admin, "is_superuser": admin},
        )
        if created or reset:
            obj.set_password(password)
            obj.save()
        self.stdout.write(f"{'Created' if created else 'Exists '} user {obj.username}{' (admin)' if admin else ''}")
        return obj

    def _seed_categories(self, owner):
        result = {}
        for name, kind in PREDEFINED_CATEGORIES:
            # Case-insensitive lookup: the DB constraint is unique on (lower(name), owner, kind).
            obj = Category.objects.filter(owner=owner, kind=kind, name__iexact=name).first()
            if obj is None:
                obj = Category.objects.create(owner=owner, name=name, kind=kind)
            result[name] = obj
        self.stdout.write(f"Categories ready: {len(result)}")
        return result

    def _seed_transactions(self, owner, categories):
        created = 0
        for days_ago, cat_name, amount, description in SAMPLE_TRANSACTIONS:
            category = categories[cat_name]
            # The date is not part of the lookup, so re-running on another day does not duplicate rows.
            _, was_created = Transaction.objects.get_or_create(
                owner=owner,
                category=category,
                kind=category.kind,
                amount=Decimal(amount),
                description=description,
                defaults={"date": date.today() - timedelta(days=days_ago)},
            )
            created += was_created
        self.stdout.write(f"Transactions created: {created}")
