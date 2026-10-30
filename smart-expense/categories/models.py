from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower


class Category(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    KINDS = [(INCOME, "Income"), (EXPENSE, "Expense")]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    kind = models.CharField(max_length=7, choices=KINDS)

    class Meta:
        ordering = ["kind", "name"]
        constraints = [models.UniqueConstraint(Lower("name"), "owner", "kind", name="category_unique_name")]

    def clean(self):
        if self.pk and self.transactions.exclude(kind=self.kind).exists():
            raise ValidationError("Cannot change the type of a category with existing transactions.")
        if self.pk and self.kind != self.EXPENSE and self.budgets.exists():
            raise ValidationError("A budget category must remain an expense category.")

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"
