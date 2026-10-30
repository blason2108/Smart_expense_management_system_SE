"""Seed demo/test data (FND-05): standard + admin users, predefined categories, sample transactions.

Usage:  python manage.py seed_data [--force] [--reset]

* Idempotent: running it twice does not create duplicates.
* Refuses to run when DEBUG is False unless --force (the seeded passwords are well known).
* Passwords come from SEED_USER_PASSWORD / SEED_ADMIN_PASSWORD (dev defaults below).
* Categories/transactions are seeded only if those models exist and have the expected fields;
  otherwise they are skipped with a warning (their modules are built in other issues).
"""
import os
from datetime import date, timedelta
from decimal import Decimal

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

STANDARD_USER = {"username": "user1", "email": "user1@example.com"}
ADMIN_USER = {"username": "admin1", "email": "admin1@example.com"}

# (name, type) - type is "income" or "expense"
PREDEFINED_CATEGORIES = [
    ("Salary", "income"), ("Freelance", "income"),
    ("Food", "expense"), ("Transport", "expense"), ("Rent", "expense"),
    ("Utilities", "expense"), ("Entertainment", "expense"), ("Health", "expense"),
    ("Shopping", "expense"),
]

# (days_ago, category name, type, amount, description)
SAMPLE_TRANSACTIONS = [
    (28, "Salary", "income", "50000.00", "Monthly salary"),
    (25, "Rent", "expense", "15000.00", "Monthly rent"),
    (20, "Food", "expense", "850.50", "Groceries"),
    (14, "Transport", "expense", "400.00", "Metro card top-up"),
    (9, "Utilities", "expense", "1200.00", "Electricity bill"),
    (5, "Entertainment", "expense", "600.00", "Movie night"),
    (2, "Food", "expense", "320.00", "Lunch"),
]


def _field_names(model):
    return {f.name for f in model._meta.get_fields()}


def _first(names, *candidates):
    return next((c for c in candidates if c in names), None)


class Command(BaseCommand):
    help = "Seed standard + admin users, predefined categories and sample transactions."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Allow running when DEBUG is False.")
        parser.add_argument("--reset", action="store_true", help="Reset seeded users' passwords.")

    def handle(self, *args, **opts):
        if not settings.DEBUG and not opts["force"]:
            raise CommandError("Refusing to seed with DEBUG=False. Use --force if you really mean it.")
        user = self._seed_user(STANDARD_USER, os.environ.get("SEED_USER_PASSWORD", "User#12345"), opts["reset"])
        self._seed_user(
            ADMIN_USER, os.environ.get("SEED_ADMIN_PASSWORD", "Admin#12345"), opts["reset"], admin=True
        )
        categories = self._seed_categories(user)
        self._seed_transactions(user, categories)
        self.stdout.write(self.style.SUCCESS("Seed data complete."))

    def _seed_user(self, data, password, reset, admin=False):
        User = get_user_model()
        obj, created = User.objects.get_or_create(
            username=data["username"],
            defaults={"email": data["email"], "is_staff": admin, "is_superuser": admin},
        )
        if created or reset:
            obj.set_password(password)
            obj.save()
        self.stdout.write(f"{'Created' if created else 'Exists '} user {obj.username}{' (admin)' if admin else ''}")
        return obj

    def _seed_categories(self, owner):
        try:
            Category = apps.get_model("categories", "Category")
        except LookupError:
            self.stdout.write(self.style.WARNING("categories.Category not found - skipping categories."))
            return {}
        names = _field_names(Category)
        type_field = _first(names, "category_type", "type", "kind")
        flag_field = _first(names, "is_predefined", "is_default", "is_system")
        if "name" not in names:
            self.stdout.write(self.style.WARNING("Category has no 'name' field - skipping categories."))
            return {}
        user_field = Category._meta.get_field("user") if "user" in names else None
        result = {}
        for name, ctype in PREDEFINED_CATEGORIES:
            lookup = {"name": name}
            defaults = {}
            if type_field:
                defaults[type_field] = ctype
            if flag_field:
                defaults[flag_field] = True
            if user_field is not None:
                (defaults if user_field.null else lookup)["user"] = None if user_field.null else owner
            obj, _ = Category.objects.get_or_create(**lookup, defaults=defaults)
            result[name] = obj
        self.stdout.write(f"Categories ready: {len(result)}")
        return result

    def _seed_transactions(self, user, categories):
        try:
            Txn = apps.get_model("transactions", "Transaction")
        except LookupError:
            self.stdout.write(self.style.WARNING("transactions.Transaction not found - skipping transactions."))
            return
        names = _field_names(Txn)
        if not categories or not {"user", "category", "amount", "date"} <= names:
            self.stdout.write(self.style.WARNING("Transaction model not ready - skipping transactions."))
            return
        type_field = _first(names, "transaction_type", "type", "kind")
        desc_field = _first(names, "description", "note", "notes")
        created = 0
        for days_ago, cat, ttype, amount, desc in SAMPLE_TRANSACTIONS:
            if cat not in categories:
                continue
            lookup = {
                "user": user, "category": categories[cat],
                "amount": Decimal(amount), "date": date.today() - timedelta(days=days_ago),
            }
            defaults = {}
            if type_field:
                defaults[type_field] = ttype
            if desc_field:
                defaults[desc_field] = desc
            _, was_created = Txn.objects.get_or_create(**lookup, defaults=defaults)
            created += was_created
        self.stdout.write(f"Transactions created: {created}")
