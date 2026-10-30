from django import forms

from categories.models import Category

from .models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ["category", "start_date", "end_date", "limit", "threshold"]
        widgets = {key: forms.DateInput(attrs={"type": "date"}) for key in ["start_date", "end_date"]}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.owner = user
        self.fields["category"].queryset = Category.objects.filter(owner=user, kind=Category.EXPENSE)
