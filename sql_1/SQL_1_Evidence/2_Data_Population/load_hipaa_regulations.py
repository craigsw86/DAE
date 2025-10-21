"""
Django Management Command: load_hipaa_regulations
Load comprehensive HIPAA regulations into the database

Usage:
    python manage.py load_hipaa_regulations
    python manage.py load_hipaa_regulations --clear
    python manage.py load_hipaa_regulations --category "Security Rule"
"""

from django.core.management.base import BaseCommand, CommandError
from checklist.models import RegulationUpdate
import sys
import os

# Add the backend directory to the path to import the regulations script
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from create_comprehensive_hipaa_regulations import create_comprehensive_hipaa_regulations

class Command(BaseCommand):
    help = 'Load comprehensive HIPAA regulations into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing regulations before loading new ones',
        )
        parser.add_argument(
            '--category',
            type=str,
            help='Load only regulations from a specific category (Privacy Rule, Security Rule, Breach Notification, Enforcement, Administrative)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be loaded without actually creating records',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(' HIPAA Regulations Loader')
        )
        self.stdout.write('=' * 50)
        
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(' DRY RUN MODE - No changes will be made')
            )
            return
        
        if options['clear']:
            self.stdout.write('  Clearing existing regulations...')
            count = RegulationUpdate.objects.count()
            RegulationUpdate.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'   Deleted {count} existing regulations')
            )
        
        if options['category']:
            self.stdout.write(
                self.style.WARNING(f'  Category filtering not yet implemented - loading all regulations')
            )
        
        try:
            # Load the comprehensive regulations
            create_comprehensive_hipaa_regulations()
            
            self.stdout.write('')
            self.stdout.write(
                self.style.SUCCESS(' HIPAA regulations loaded successfully!')
            )
            
            # Show summary
            total_count = RegulationUpdate.objects.count()
            self.stdout.write(f' Total regulations in database: {total_count}')
            
            # Show categories
            categories = {}
            for reg in RegulationUpdate.objects.all():
                category = 'Other'
                if 'Privacy Rule' in reg.title:
                    category = 'Privacy Rule'
                elif 'Security Rule' in reg.title:
                    category = 'Security Rule'
                elif 'Breach Notification' in reg.title:
                    category = 'Breach Notification'
                elif 'Enforcement' in reg.title:
                    category = 'Enforcement'
                elif 'Administrative' in reg.title:
                    category = 'Administrative'
                
                categories[category] = categories.get(category, 0) + 1
            
            self.stdout.write('\n Regulations by category:')
            for category, count in categories.items():
                self.stdout.write(f'  • {category}: {count}')
                
        except Exception as e:
            raise CommandError(f'Error loading regulations: {str(e)}')
