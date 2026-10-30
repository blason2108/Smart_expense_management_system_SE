from django import forms

from categories.models import Category

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["kind", "category", "amount", "date", "description"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.owner = user
        self.fields["category"].queryset = Category.objects.filter(owner=user)


class FilterForm(forms.Form):
    month = forms.DateField(required=False, input_formats=["%Y-%m"], widget=forms.DateInput(attrs={"type": "month"}))
    start = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    end = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)
    kind = forms.ChoiceField(choices=[("", "All types")] + Category.KINDS, required=False)
    q = forms.CharField(required=False, max_length=100, label="Description search")

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(owner=user)

    def clean(self):
        data = super().clean()
        if data.get("start") and data.get("end") and data["start"] > data["end"]:
            raise forms.ValidationError("Start date must be on or before end date.")
        return data
