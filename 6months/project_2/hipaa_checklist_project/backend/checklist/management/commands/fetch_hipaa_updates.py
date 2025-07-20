from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from checklist.models import Regulation

class Command(BaseCommand):
    help = 'Scrape HHS OCR for HIPAA updates'

    def handle(self, *args, **options):
        base_url = 'https://www.hhs.gov/hipaa/for-professionals'
        subpages = ['', 'privacy/index.html', '/security/laws-regulations/index.html', '/breach-notification/index.html']
        for sub in subpages:
            url = f'{base_url}{sub}'
            try:
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                # Robust : Find main content div, then headings and paras
                content = soup.find('div', class='content') or soup.find('main')
                if content:
                    headings = content.find_all(['h2', 'h3'])
                    for heading in headings:
                        name = heading.text.strip()
                        desc = ''
                        next_p = heading.find_text('p')
                        if next_p:
                            desc = next_p.text.strip()
                        links = heading.find_next('ul').find_all('a') if heading.find_next('ul') else []
                        for link in links:
                            desc += f'{link.text.strip()} ({link["href"]})'
                        # Update or create (admin review via flag or log)
                        Regulation.objects.update_or_create(
                            name=name,
                            defaults={'description': desc, 'category': sub.split('/')[1] if '/' in sub else 'General'}
                        )
                    self.stdout.write(self.style.SUCCESS(f'Updated from {url}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error scraping {url}: {e}'))
        # Log for failures/mitigation: Fallback to manual
