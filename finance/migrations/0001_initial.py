from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="BudgetEntry", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("month", models.DateField(help_text="Первый день месяца")),
        ("category", models.CharField(max_length=100)),
        ("description", models.CharField(blank=True, max_length=250)),
        ("planned", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
        ("actual", models.DecimalField(decimal_places=2, default=0, max_digits=14)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="budget_entries", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ["month", "category"]})]
