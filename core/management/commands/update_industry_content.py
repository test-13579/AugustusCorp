from django.core.management.base import BaseCommand
from core.models import Industry


INDUSTRY_DATA = [
    {
        'name': 'Automotive',
        'icon_name': 'car',
        'description': (
            'Precision freight for OEM components, finished vehicles, and production-critical parts. '
            'Dedicated flatbeds, enclosed carriers, and just-in-time delivery keep assembly lines running '
            'across North America — zero delays, zero excuses.'
        ),
    },
    {
        'name': 'Technology & Electronics',
        'icon_name': 'chip',
        'description': (
            'Secure, time-critical shipping for semiconductors, high-value electronics, and tech hardware. '
            'White-glove handling, real-time tracking, and expedited lanes protect your cargo from factory '
            'floor to data center — anywhere in the world.'
        ),
    },
    {
        'name': 'Healthcare & Pharma',
        'icon_name': 'cross',
        'description': (
            'GDP-compliant cold chain and temperature-controlled logistics for pharmaceuticals, biologics, '
            'and medical devices. Validated reefer units, strict chain-of-custody, and 24/7 monitoring '
            'ensure product integrity from origin to patient.'
        ),
    },
    {
        'name': 'Industrial & Manufacturing',
        'icon_name': 'gear',
        'description': (
            'Heavy-haul, over-dimensional, and just-in-time freight for industrial machinery, capital '
            'equipment, and manufactured goods. Full permit management, specialized rigging, and cross-border '
            'expertise keep your production schedules on track.'
        ),
    },
    {
        'name': 'Consumer & Retail',
        'icon_name': 'bag',
        'description': (
            'High-volume transport for consumer goods from production to distribution center to retail shelf. '
            'Reliable capacity for seasonal peaks, promotional launches, and everyday replenishment — '
            'delivered on time, every time.'
        ),
    },
    {
        'name': 'Aerospace & Defense',
        'icon_name': 'plane',
        'description': (
            'Security-compliant logistics for aerospace components, defense cargo, and government freight. '
            'ITAR-registered carriers, customs clearance expertise, and cleared handling teams move '
            'sensitive loads safely across domestic and international corridors.'
        ),
    },
    {
        'name': 'Energy & Oil & Gas',
        'icon_name': 'bolt',
        'description': (
            'Specialized heavy freight for oilfield equipment, pipe, project cargo, and energy sector supplies. '
            'Dedicated permit management and over-dimensional expertise across US shale basins and '
            'UAE energy corridors keep your operations running.'
        ),
    },
    {
        'name': 'Food & Beverage',
        'icon_name': 'snowflake',
        'description': (
            'Temperature-controlled transport for fresh produce, frozen goods, and packaged foods. '
            'Multi-temp reefer fleets, FSMA-compliant carriers, and strict cold chain protocols '
            'preserve product quality from origin farm to retail shelf.'
        ),
    },
]


class Command(BaseCommand):
    help = 'Update Industry records with richer, more detailed content'

    def handle(self, *args, **options):
        updated = 0
        for data in INDUSTRY_DATA:
            try:
                ind = Industry.objects.get(name=data['name'])
                ind.description = data['description']
                ind.icon_name = data['icon_name']
                ind.save(update_fields=['description', 'icon_name'])
                self.stdout.write(self.style.SUCCESS(f'  Updated: {ind.name}'))
                updated += 1
            except Industry.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Not found: {data["name"]} — skipping'))

        self.stdout.write(self.style.SUCCESS(f'\nDone. {updated}/{len(INDUSTRY_DATA)} industries updated.'))
