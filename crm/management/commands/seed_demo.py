"""Create isolated, reproducible demo data for a single existing user."""
import random
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from crm.models import Client, Deal, Task
from sales.models import Company, Lead
from ._demo_utils import marker

FIRST = ("Алина", "Данияр", "Айгерим", "Арман", "Мария", "Тимур", "Аружан", "Максим")
LAST = ("Садыкова", "Нурланов", "Ибраева", "Ким", "Серик", "Ахметов", "Пак", "Сулейменова")
BRANDS = ("Nomad", "Orda", "Steppe", "Qazaq", "Astana", "Digital", "Prime", "Vertex")
SECTORS = ("IT", "Розница", "Логистика", "Услуги", "Образование")

class Command(BaseCommand):
    help = "Create clearly tagged OCTAX demo companies, clients, leads, deals and tasks"

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True, help="Existing username to own demo records")
        parser.add_argument("--batch", default="default", help="Demo batch label")
        parser.add_argument("--companies", type=int, default=10)
        parser.add_argument("--clients", type=int, default=30)
        parser.add_argument("--leads", type=int, default=20)
        parser.add_argument("--deals", type=int, default=20)
        parser.add_argument("--tasks", type=int, default=20)
        parser.add_argument("--seed", type=int, default=42)

    @transaction.atomic
    def handle(self, *args, **options):
        tag = marker(options["batch"])
        for key in ("companies", "clients", "leads", "deals", "tasks"):
            if not 0 <= options[key] <= 1000:
                raise CommandError(f"--{key} must be between 0 and 1000")
        user = get_user_model().objects.filter(username=options["user"]).first()
        if user is None:
            raise CommandError("User does not exist. Create one with createsuperuser first.")
        # Reject duplicate batches; never overwrite or duplicate user data.
        if (Company.objects.filter(owner=user, notes=tag).exists() or
            Client.objects.filter(owner=user, notes=tag).exists() or
            Lead.objects.filter(owner=user, notes=tag).exists() or
            Deal.objects.filter(owner=user, title__startswith=tag + " ").exists() or
            Task.objects.filter(owner=user, description=tag).exists()):
            raise CommandError(f"Demo batch '{options['batch']}' already exists for this user. Clear it first or choose another --batch.")
        rng = random.Random(options["seed"])
        companies = []
        for i in range(options["companies"]):
            companies.append(Company.objects.create(owner=user, name=f"{rng.choice(BRANDS)} {i+1:03d} {options['batch']}", industry=rng.choice(SECTORS), city="Астана", notes=tag))
        clients = []
        for i in range(options["clients"]):
            clients.append(Client.objects.create(owner=user, name=f"{rng.choice(FIRST)} {rng.choice(LAST)} {i+1:03d}", city="Астана", email=f"demo.{options['batch']}.{i+1}@example.test", notes=tag))
        for i in range(options["leads"]):
            Lead.objects.create(owner=user, name=f"{rng.choice(FIRST)} {rng.choice(LAST)} {i+1:03d}", company=rng.choice(companies) if companies else None, status=rng.choice([Lead.Status.NEW, Lead.Status.CONTACTED, Lead.Status.QUALIFIED]), source=rng.choice(Lead.Source.values), notes=tag)
        for i in range(options["deals"]):
            if not clients:
                raise CommandError("Deals require clients: use --clients 1 or more, or --deals 0")
            Deal.objects.create(owner=user, client=rng.choice(clients), title=f"{tag} Сделка {i+1:03d}", amount=Decimal(rng.randrange(20_000, 1_000_000)), status=rng.choice(Deal.Status.values), expected_close_date=timezone.localdate()+timedelta(days=rng.randint(1,90)))
        for i in range(options["tasks"]):
            Task.objects.create(owner=user, client=rng.choice(clients) if clients else None, title=f"Демо-задача {i+1:03d}", description=tag, priority=rng.choice(Task.Priority.values), due_date=timezone.localdate()+timedelta(days=rng.randint(1,30)))
        self.stdout.write(self.style.SUCCESS(f"Created batch {options['batch']} for {user.username}: " + ", ".join(f"{options[k]} {k}" for k in ("companies", "clients", "leads", "deals", "tasks"))))
