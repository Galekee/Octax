"""Remove only OCTAX demo records for a selected owner and batch."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from crm.models import Client, Deal, Task
from sales.models import Company, Lead
from ._demo_utils import marker

class Command(BaseCommand):
    help = "Delete a tagged demo batch only (requires --confirm)"

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--batch", default="default")
        parser.add_argument("--confirm", action="store_true", help="Actually delete matching demo records")

    @transaction.atomic
    def handle(self, *args, **options):
        tag = marker(options["batch"])
        user = get_user_model().objects.filter(username=options["user"]).first()
        if user is None:
            raise CommandError("User does not exist")
        # Important: never delete real records that reference demo clients or companies.
        companies = Company.objects.filter(owner=user, notes=tag)
        clients = Client.objects.filter(owner=user, notes=tag)
        leads = Lead.objects.filter(owner=user, notes=tag)
        deals = Deal.objects.filter(owner=user, title__startswith=tag + " ")
        tasks = Task.objects.filter(owner=user, description=tag)
        counts = {"companies": companies.count(), "clients": clients.count(), "leads": leads.count(), "deals": deals.count(), "tasks": tasks.count()}
        self.stdout.write("Matching demo records: " + ", ".join(f"{k}={v}" for k,v in counts.items()))
        if not options["confirm"]:
            self.stdout.write("Preview only. Add --confirm to delete.")
            return
        # Protect user-created records connected to demo data.
        from crm.models import PortalRequest, ClientPortalProfile
        if (Deal.objects.filter(client__in=clients).exclude(pk__in=deals.values("pk")).exists() or
            Task.objects.filter(client__in=clients).exclude(pk__in=tasks.values("pk")).exists() or
            ClientPortalProfile.objects.filter(client__in=clients).exists() or
            PortalRequest.objects.filter(resulting_deal__in=deals).exists() or
            PortalRequest.objects.filter(resulting_task__in=tasks).exists() or
            Lead.objects.filter(company__in=companies).exclude(pk__in=leads.values("pk")).exists() or
            Lead.objects.filter(converted_client__in=clients).exclude(pk__in=leads.values("pk")).exists()):
            raise CommandError("Some demo records are linked to non-demo data. Cleanup cancelled to protect real records.")
        # Order matters: avoid cascading deletion of unrelated data.
        leads.delete()
        deals.delete()
        tasks.delete()
        clients.delete()
        companies.delete()
        self.stdout.write(self.style.SUCCESS("Demo batch removed; other batches and real records preserved."))
