from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from categories.models import Category


class Transaction(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    kind = models.CharField(max_length=7, choices=Category.KINDS)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    date = models.DateField(db_index=True)
    description = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ["-date", "-pk"]
        constraints = [models.CheckConstraint(condition=models.Q(amount__gt=0), name="transaction_positive")]
        indexes = [models.Index(fields=["owner", "date"])]

    def clean(self):
        if self.category_id:
            if self.category.owner_id != self.owner_id:
                raise ValidationError({"category": "Choose your own category."})
            if self.category.kind != self.kind:
                raise ValidationError({"category": "Category type must match transaction type."})
