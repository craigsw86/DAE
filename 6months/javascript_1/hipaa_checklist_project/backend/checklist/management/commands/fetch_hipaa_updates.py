from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from checklist.models import RegulationUpdate

class Command(BaseCommand):
    help = 'Fetch HIPAA updates from HHS OCR'

    def handle(self, *args, **options):
        url = 'https://www.hhs.gov/hipaa/for-professionals/index.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape 'Recent Updates' or 'Guidance' section (based on 2025 structure: ul with class 'guidance-list')
        updates = soup.find_all('li', class_='guidance-item')  # Robust selector; mitigate risk with logs
        for update in updates:
            title = update.find('a').text.strip()
            desc = update.find('p').text.strip()
            link = 'https://www.hhs.gov' + update.find('a')['href']
            pub_date_str = update.find('span', class_='date').text
            pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d').date()

            # Insert if new (prevent duplicates)
            if not RegulationUpdate.objects.filter(title=title).exists():
                RegulationUpdate.objects.create(
                    title=title, description=desc, source_url=link, pub_date=pub_date
                )
                self.stdout.write(self.style.SUCCESS(f'Added: {title}'))

        # Governance: Log scrape success (integrate with Wazuh via syslogs)
        self.stdout.write(self.style.SUCCESS('Scrape complete'))