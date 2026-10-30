import os
from datetime import date

from django.core.management.base import BaseCommand, CommandError

from accounts.models import User
from budgets.models import Budget
from categories.models import Category
from transactions.models import Transaction


class Command(BaseCommand):
    help = "Create isolated demo data; requires DEMO_PASSWORD. Does not reset existing passwords."

    def handle(self, *args, **options):
        password = os.environ.get("DEMO_PASSWORD")
        if not password or len(password) < 12:
            raise CommandError("Set DEMO_PASSWORD to at least 12 characters.")
        user, created = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.test"})
        if created:
            user.set_password(password)
            user.save()
        income, _ = Category.objects.get_or_create(owner=user, name="Salary", kind="income")
        food, _ = Category.objects.get_or_create(owner=user, name="Food", kind="expense")
        for cat, amount, description in [(income, "30000.00", "Demo salary"), (food, "850.00", "Demo groceries")]:
            Transaction.objects.get_or_create(
                owner=user, category=cat, kind=cat.kind, amount=amount, date=date(2026, 10, 20), description=description
            )
        Budget.objects.get_or_create(
            owner=user,
            category=food,
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 31),
            defaults={"limit": "1000.00", "threshold": 80},
        )
        self.stdout.write(self.style.SUCCESS("Demo data ready for username demo."))
