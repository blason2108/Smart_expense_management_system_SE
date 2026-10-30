from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "kind"]

    def clean(self):
        data = super().clean()
        if data.get("name") and data.get("kind"):
            duplicate = Category.objects.filter(owner=self.instance.owner, name__iexact=data["name"], kind=data["kind"])
            if self.instance.pk:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                self.add_error("name", "This category already exists.")
        return data
