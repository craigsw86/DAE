from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail
from checklist.models import ChecklistItem, RegulationUpdate
from django.utils import timezone
import logging

class Command(BaseCommand):
    help = 'Monitor risks and send alerts if thresholds are exceeded.'

    def handle(self, *args, **options):
        # Example: High risk = incomplete checklist item with a regulation update in the last 30 days
        now = timezone.now()
        high_risks = ChecklistItem.objects.filter(completed=False, regulation_update__created_at__gte=now - timezone.timedelta(days=30))
        overdue_risks = ChecklistItem.objects.filter(completed=False, last_updated__lte=now - timezone.timedelta(days=60))

        alert_msgs = []
        if high_risks.exists():
            alert_msgs.append(f"High risks detected: {high_risks.count()} incomplete items for recent regulations.")
        if overdue_risks.exists():
            alert_msgs.append(f"Overdue risks detected: {overdue_risks.count()} items not updated in 60+ days.")

        if alert_msgs:
            alert_text = '\n'.join(alert_msgs)
            # Log to file
            logging.basicConfig(filename='risk_alerts.log', level=logging.INFO)
            logging.info(f"[ALERT] {alert_text}")
            # Email superusers
            superusers = User.objects.filter(is_superuser=True)
            emails = [u.email for u in superusers if u.email]
            if emails:
                send_mail(
                    subject='[ALERT] Risk Monitoring Notification',
                    message=alert_text,
                    from_email='noreply@hipaachecklist.local',
                    recipient_list=emails,
                    fail_silently=True,
                )
            self.stdout.write(self.style.WARNING(alert_text))
        else:
            self.stdout.write(self.style.SUCCESS('No high or overdue risks detected.'))
