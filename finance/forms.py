from django import forms
from .models import BudgetEntry

class BudgetEntryForm(forms.ModelForm):
    class Meta:
        model = BudgetEntry
        fields = ["month", "category", "description", "planned", "actual"]
        widgets = {"month": forms.DateInput(attrs={"type": "date"})}

    def clean_month(self):
        value = self.cleaned_data["month"]
        return value.replace(day=1)
