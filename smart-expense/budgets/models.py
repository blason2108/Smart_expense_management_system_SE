from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum

from categories.models import Category
from transactions.models import Transaction


class Budget(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="budgets")
    start_date = models.DateField()
    end_date = models.DateField()
    limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    threshold = models.PositiveSmallIntegerField(default=80, validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        ordering = ["-start_date", "pk"]
        constraints = [
            models.CheckConstraint(condition=models.Q(limit__gt=0), name="budget_positive"),
            models.CheckConstraint(condition=models.Q(end_date__gte=models.F("start_date")), name="budget_dates"),
            models.CheckConstraint(condition=models.Q(threshold__gte=1, threshold__lte=100), name="budget_threshold"),
        ]

    def clean(self):
        if self.category_id and (self.category.owner_id != self.owner_id or self.category.kind != Category.EXPENSE):
            raise ValidationError({"category": "Choose your own expense category."})
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({"end_date": "End date must be on or after start date."})

    @property
    def spent(self):
        return Transaction.objects.filter(
            owner=self.owner,
            category=self.category,
            kind=Category.EXPENSE,
            date__range=(self.start_date, self.end_date),
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    @property
    def progress(self):
        return self.spent / self.limit * 100

    @property
    def status(self):
        value = self.progress
        return "Exceeded" if value > 100 else ("Warning" if value >= self.threshold else "On track")
