from django.conf import settings
from django.db import models

class BudgetEntry(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budget_entries")
    month = models.DateField(help_text="Первый день месяца")
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True)
    planned = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    actual = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["month", "category"]

    def __str__(self):
        return f"{self.month} / {self.category}"
