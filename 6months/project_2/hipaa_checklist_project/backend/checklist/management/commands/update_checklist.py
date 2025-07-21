from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from checklist.models import RegulationUpdate, ChecklistItem

class Command(BaseCommand):
    help = 'Map updates to user checklists'

    def handle(self, *args, **options):
        new_updates = RegulationUpdate.objects.filter(checklistitem__isnull=True)
        for user in User.objects.all():
            for update in new_updates:
                ChecklistItem.objects.get_or_create(
                    user=user, regulation_update=update
                )
        self.stdout.write(self.style.SUCCESS('Checklists updated'))