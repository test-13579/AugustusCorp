from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from core.models import (
    Service, Testimonial, TeamMember, BlogPost, Company, Shipment,
    TrackingEvent, Job, SiteSettings, FaqItem, Commitment, Industry,
    AboutHighlight, WhyUsFeature, ShipmentType, SupportChannel, Office, CareerPerk,
    CalcService, CalcZone, CalcRoute, PortCity,
    TruckType, CargoType,
)


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        self._site_settings()
        self._truck_cargo()
        self._calculator()
        self._services()
        self._shipment_types()
        self._why_us_features()
        self._commitments()
        self._about_highlights()
        self._industries()
        self._support_channels()
        self._offices()
        self._career_perks()
        self._faq()
        self._testimonials()
        self._team()
        self._blog()
        self._companies()
        self._shipments()
        self._jobs()
        self.stdout.write(self.style.SUCCESS('✓ Database seeded successfully!'))
        self.stdout.write('Admin: python manage.py createsuperuser')
        self.stdout.write('Run:   python manage.py runserver')

    def _site_settings(self):
        SiteSettings.objects.all().delete()
        SiteSettings.objects.create(
            pk=1,
            company_name     = 'Augustus Corp',
            tagline          = 'Trucking & Brokerage Solutions — Reliable · Scalable · On-Time',
            wordmark_main    = 'AUGUST',
            wordmark_accent  = 'US',
            wordmark_sub     = 'CORP',
            phone            = '803-666-8368',
            email            = 'garry@augustusbrokerage.com',
            address          = 'United States & Canada',
            website          = 'augustustransport.com',
            hours_weekday    = '8am–6pm ET',
            hours_saturday   = '9am–2pm ET',
            footer_blurb     = 'Nationwide trucking & freight solutions across all 48 U.S. states and Canada. OTR, Drayage, Warehousing & Cross-Border — backed by a vetted carrier network.',
            meta_description = 'Augustus Corp — End-to-end logistics solutions. Reliable, scalable, on-time freight across the US and Canada. OTR, Drayage, Warehousing & Cross-Border.',
        )
        self.stdout.write('  ✓ Site settings')

    def _truck_cargo(self):
        TruckType.objects.all().delete()
        CargoType.objects.all().delete()

        trucks = [
            ('Dry Van 53\'',        'dry-van',     'Standard enclosed trailer for general freight',         '44,000 lbs / 2,700 cu ft', 2.80, 600,  25.00, 1),
            ('Reefer 53\'',         'reefer',       'Temperature-controlled trailer for perishables',        '43,000 lbs / 2,700 cu ft', 3.50, 850,  25.00, 2),
            ('Flatbed 48\'',        'flatbed',      'Open deck for oversized, machinery or building loads',  '48,000 lbs / 48 ft deck',  3.20, 750,  25.00, 3),
            ('Step Deck',           'step-deck',    'Lower deck height for taller cargo',                    '46,000 lbs / 53 ft deck',  3.40, 800,  25.00, 4),
            ('Box Truck 26\'',      'box-truck',    'Medium freight — city deliveries and LTL',              '12,500 lbs / 1,700 cu ft', 2.20, 350,  20.00, 5),
            ('Sprinter Van',        'sprinter',     'Expedited small freight and urgent loads',              '3,500 lbs / 270 cu ft',    1.80, 200,  20.00, 6),
            ('Lowboy / Heavy Haul', 'lowboy',       'Heavy machinery, equipment, and oversized loads',       '80,000 lbs+',              4.50, 1200, 30.00, 7),
        ]
        for name, key, desc, cap, rpm, mc, fsp, order in trucks:
            TruckType.objects.create(name=name, key=key, description=desc, capacity=cap,
                                     rate_per_mile=rpm, min_charge=mc, fuel_surcharge_pct=fsp, order=order)
        self.stdout.write('  ✓ Truck types')

        cargos = [
            ('General Freight',         'general',      'Standard palletized or boxed cargo',                      1.00, 1),
            ('Food & Beverage',         'food',         'Temperature-sensitive food and beverage products',        1.15, 2),
            ('Electronics',             'electronics',  'High-value electronic equipment and components',          1.20, 3),
            ('Automotive Parts',        'automotive',   'Vehicle parts, components and accessories',               1.10, 4),
            ('Building Materials',      'building',     'Construction materials, lumber, steel',                   1.00, 5),
            ('Medical / Pharma',        'medical',      'Medical devices, pharmaceuticals and healthcare products', 1.35, 6),
            ('Fragile / High Value',    'fragile',      'Art, antiques or high-value fragile items',               1.30, 7),
            ('Hazardous Materials',     'hazmat',       'DOT-regulated hazardous materials (HAZMAT)',               1.50, 8),
            ('Oversized / Heavy Haul',  'oversized',    'Machinery, equipment or loads requiring special permits',  1.80, 9),
            ('Perishables (Reefer)',    'perishables',  'Fresh produce, frozen goods and cold-chain freight',       1.25, 10),
        ]
        for name, key, desc, mult, order in cargos:
            CargoType.objects.create(name=name, key=key, description=desc, multiplier=mult, order=order)
        self.stdout.write('  ✓ Cargo types')

    def _calculator(self):
        CalcService.objects.all().delete()
        CalcRoute.objects.all().delete()
        PortCity.objects.all().delete()
        CalcZone.objects.all().delete()

        # ── Services ──────────────────────────────────────────────────────────
        svc_data = [
            ('Full Truckload (FTL)',            'ftl',        2200, 'per load',   1),
            ('Less Than Truckload (LTL)',       'ltl',        320,  'per pallet', 2),
            ('Drayage (Port / Rail)',           'drayage',    450,  'per move',   3),
            ('Reefer (Temperature-Controlled)', 'reefer',     2800, 'per load',   4),
            ('Intermodal (Rail + Truck)',       'intermodal', 1600, 'per load',   5),
            ('Heavy-Haul & Specialized',       'heavy-haul', 3500, 'per load',   6),
            ('Cross-Border US–Canada',         'cross-border',2600,'per load',   7),
        ]
        for name, key, rate, unit, order in svc_data:
            CalcService.objects.create(name=name, key=key, base_rate=rate, unit_label=unit, order=order)
        self.stdout.write('  ✓ Calc services')

        # ── Zones ─────────────────────────────────────────────────────────────
        zone_data = [
            ('West Coast USA',        'west-coast-usa',  1),
            ('East Coast USA',        'east-coast-usa',  2),
            ('South USA',             'south-usa',       3),
            ('Midwest USA',           'midwest-usa',     4),
            ('Mountain / Southwest',  'mountain-usa',    5),
            ('Canada',                'canada',          6),
            ('Mexico',                'mexico',          7),
            ('Europe',                'europe',          8),
            ('Asia Pacific',          'asia-pacific',    9),
            ('Middle East',           'middle-east',    10),
            ('Latin America',         'latin-america',  11),
            ('Africa',                'africa',         12),
        ]
        zones = {}
        for name, key, order in zone_data:
            zones[key] = CalcZone.objects.create(name=name, key=key, order=order)
        self.stdout.write('  ✓ Calc zones')

        # ── Route matrix (multiplier, transit_days) ────────────────────────
        # Rows = origin zone keys, Cols = dest zone keys
        zk = ['west-coast-usa','east-coast-usa','south-usa','midwest-usa','mountain-usa',
               'canada','mexico','europe','asia-pacific','middle-east','latin-america','africa']

        mult = [
            # WC      EC      SO      MW      MT      CA      MX      EU      AP      ME      LA      AF
            [0.40,   1.30,   1.10,   1.00,   0.60,   1.60,   1.20,   3.50,   3.00,   4.00,   2.50,   4.50],  # WC
            [1.30,   0.40,   0.80,   0.70,   1.10,   1.50,   1.40,   3.00,   3.50,   4.50,   2.00,   4.00],  # EC
            [1.10,   0.80,   0.40,   0.90,   0.90,   1.80,   0.90,   3.20,   3.80,   4.20,   1.80,   4.20],  # SO
            [1.00,   0.70,   0.90,   0.35,   0.80,   1.60,   1.30,   3.30,   3.60,   4.30,   2.20,   4.30],  # MW
            [0.60,   1.10,   0.90,   0.80,   0.40,   1.70,   1.00,   3.60,   3.20,   4.10,   2.40,   4.60],  # MT
            [1.60,   1.50,   1.80,   1.60,   1.70,   0.50,   1.90,   4.00,   3.80,   4.80,   3.00,   5.00],  # CA
            [1.20,   1.40,   0.90,   1.30,   1.00,   1.90,   0.50,   4.20,   4.00,   4.50,   1.50,   4.80],  # MX
            [3.50,   3.00,   3.20,   3.30,   3.60,   4.00,   4.20,   0.80,   2.00,   2.50,   3.50,   2.00],  # EU
            [3.00,   3.50,   3.80,   3.60,   3.20,   3.80,   4.00,   2.00,   0.80,   1.50,   4.00,   3.00],  # AP
            [4.00,   4.50,   4.20,   4.30,   4.10,   4.80,   4.50,   2.50,   1.50,   0.80,   4.50,   2.50],  # ME
            [2.50,   2.00,   1.80,   2.20,   2.40,   3.00,   1.50,   3.50,   4.00,   4.50,   0.70,   4.20],  # LA
            [4.50,   4.00,   4.20,   4.30,   4.60,   5.00,   4.80,   2.00,   3.00,   2.50,   4.20,   0.90],  # AF
        ]
        transit = [
            # WC      EC      SO      MW       MT      CA       MX      EU           AP           ME           LA           AF
            ['1–2',  '5–7',  '3–5',  '3–5',  '1–3',  '3–6',  '2–5',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['5–7',  '1–2',  '2–4',  '2–3',  '4–6',  '3–5',  '4–6',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['3–5',  '2–4',  '1–2',  '2–4',  '2–4',  '4–7',  '2–4',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['3–5',  '2–3',  '2–4',  '1–2',  '2–4',  '3–5',  '3–5',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['1–3',  '4–6',  '2–4',  '2–4',  '1–2',  '3–6',  '2–4',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['3–6',  '3–5',  '4–7',  '3–5',  '3–6',  '1–2',  '3–5',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['2–5',  '4–6',  '2–4',  '3–5',  '2–4',  '3–5',  '1–2',  'Contact us','Contact us','Contact us','Contact us','Contact us'],
            ['Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','1–3','2–4','2–4','3–5','2–4'],
            ['Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','2–4','1–3','2–3','4–6','3–5'],
            ['Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','2–4','2–3','1–2','4–6','2–4'],
            ['Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','3–5','4–6','4–6','1–3','4–6'],
            ['Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','Contact us','2–4','3–5','2–4','4–6','1–3'],
        ]
        for i, ok in enumerate(zk):
            for j, dk in enumerate(zk):
                CalcRoute.objects.create(
                    origin_zone=zones[ok], dest_zone=zones[dk],
                    multiplier=mult[i][j], transit_days=transit[i][j],
                )
        self.stdout.write('  ✓ Calc routes (144 lanes)')

        # ── Port Cities with Coordinates ──────────────────────────────────────
        # (name, country, zone_key, lat, lng)
        city_data = [
            # USA West Coast
            ('Los Angeles',      'USA', 'west-coast-usa',  34.052,  -118.244),
            ('Long Beach',       'USA', 'west-coast-usa',  33.771,  -118.194),
            ('Oakland',          'USA', 'west-coast-usa',  37.804,  -122.271),
            ('Seattle',          'USA', 'west-coast-usa',  47.606,  -122.332),
            ('Tacoma',           'USA', 'west-coast-usa',  47.253,  -122.444),
            ('Portland',         'USA', 'west-coast-usa',  45.523,  -122.676),
            ('San Diego',        'USA', 'west-coast-usa',  32.715,  -117.157),
            ('San Francisco',    'USA', 'west-coast-usa',  37.775,  -122.419),
            ('Stockton',         'USA', 'west-coast-usa',  37.958,  -121.291),
            ('Sacramento',       'USA', 'west-coast-usa',  38.582,  -121.494),
            # USA East Coast
            ('New York',         'USA', 'east-coast-usa',  40.713,   -74.006),
            ('Newark',           'USA', 'east-coast-usa',  40.735,   -74.172),
            ('Baltimore',        'USA', 'east-coast-usa',  39.290,   -76.612),
            ('Norfolk',          'USA', 'east-coast-usa',  36.851,   -76.285),
            ('Philadelphia',     'USA', 'east-coast-usa',  39.952,   -75.164),
            ('Boston',           'USA', 'east-coast-usa',  42.358,   -71.064),
            ('Jacksonville',     'USA', 'east-coast-usa',  30.332,   -81.656),
            ('Miami',            'USA', 'east-coast-usa',  25.775,   -80.208),
            ('Port Everglades',  'USA', 'east-coast-usa',  26.083,   -80.116),
            ('Savannah',         'USA', 'east-coast-usa',  32.078,   -81.099),
            ('Charleston',       'USA', 'east-coast-usa',  32.777,   -79.931),
            ('Wilmington',       'USA', 'east-coast-usa',  34.226,   -77.945),
            ('Brunswick',        'USA', 'east-coast-usa',  31.150,   -81.491),
            ('Tampa',            'USA', 'east-coast-usa',  27.950,   -82.457),
            # USA South
            ('Houston',          'USA', 'south-usa',       29.760,   -95.370),
            ('New Orleans',      'USA', 'south-usa',       29.951,   -90.072),
            ('Corpus Christi',   'USA', 'south-usa',       27.801,   -97.397),
            ('Beaumont',         'USA', 'south-usa',       30.086,   -94.102),
            ('Galveston',        'USA', 'south-usa',       29.301,   -94.798),
            ('Mobile',           'USA', 'south-usa',       30.694,   -88.043),
            ('Dallas',           'USA', 'south-usa',       32.776,   -96.797),
            ('Memphis',          'USA', 'south-usa',       35.149,   -90.049),
            ('Atlanta',          'USA', 'south-usa',       33.749,   -84.388),
            ('Nashville',        'USA', 'south-usa',       36.162,   -86.781),
            ('San Antonio',      'USA', 'south-usa',       29.425,   -98.494),
            ('Baton Rouge',      'USA', 'south-usa',       30.451,   -91.188),
            # USA Midwest
            ('Chicago',          'USA', 'midwest-usa',     41.878,   -87.630),
            ('Detroit',          'USA', 'midwest-usa',     42.331,   -83.046),
            ('Cleveland',        'USA', 'midwest-usa',     41.499,   -81.695),
            ('Columbus',         'USA', 'midwest-usa',     39.961,   -82.999),
            ('Indianapolis',     'USA', 'midwest-usa',     39.768,   -86.158),
            ('Milwaukee',        'USA', 'midwest-usa',     43.039,   -87.907),
            ('Minneapolis',      'USA', 'midwest-usa',     44.980,   -93.265),
            ('Kansas City',      'USA', 'midwest-usa',     39.100,   -94.578),
            ('St. Louis',        'USA', 'midwest-usa',     38.627,   -90.198),
            ('Cincinnati',       'USA', 'midwest-usa',     39.103,   -84.512),
            ('Pittsburgh',       'USA', 'midwest-usa',     40.440,   -79.996),
            ('Toledo',           'USA', 'midwest-usa',     41.663,   -83.556),
            ('Duluth',           'USA', 'midwest-usa',     46.786,   -92.101),
            # USA Mountain / Southwest
            ('Phoenix',          'USA', 'mountain-usa',    33.448,  -112.074),
            ('Denver',           'USA', 'mountain-usa',    39.739,  -104.984),
            ('Las Vegas',        'USA', 'mountain-usa',    36.175,  -115.137),
            ('Salt Lake City',   'USA', 'mountain-usa',    40.760,  -111.891),
            ('Albuquerque',      'USA', 'mountain-usa',    35.085,  -106.651),
            ('El Paso',          'USA', 'mountain-usa',    31.758,  -106.487),
            ('Tucson',           'USA', 'mountain-usa',    32.222,  -110.927),
            ('Reno',             'USA', 'mountain-usa',    39.529,  -119.814),
            ('Boise',            'USA', 'mountain-usa',    43.616,  -116.201),
            # Canada
            ('Vancouver',        'Canada', 'canada',       49.283,  -123.121),
            ('Prince Rupert',    'Canada', 'canada',       54.316,  -130.319),
            ('Toronto',          'Canada', 'canada',       43.651,   -79.347),
            ('Montreal',         'Canada', 'canada',       45.501,   -73.567),
            ('Halifax',          'Canada', 'canada',       44.649,   -63.575),
            ('Hamilton',         'Canada', 'canada',       43.256,   -79.869),
            ('Calgary',          'Canada', 'canada',       51.045,  -114.072),
            ('Edmonton',         'Canada', 'canada',       53.546,  -113.490),
            ('Winnipeg',         'Canada', 'canada',       49.895,   -97.138),
            ('Quebec City',      'Canada', 'canada',       46.813,   -71.208),
            ('Thunder Bay',      'Canada', 'canada',       48.380,   -89.246),
            # Mexico
            ('Manzanillo',       'Mexico', 'mexico',       19.052,  -104.315),
            ('Lazaro Cardenas',  'Mexico', 'mexico',       17.958,  -102.197),
            ('Veracruz',         'Mexico', 'mexico',       19.174,   -96.134),
            ('Altamira',         'Mexico', 'mexico',       22.400,   -97.917),
            ('Ensenada',         'Mexico', 'mexico',       31.867,  -116.596),
            ('Tijuana',          'Mexico', 'mexico',       32.514,  -117.038),
            ('Guadalajara',      'Mexico', 'mexico',       20.659,  -103.350),
            ('Mexico City',      'Mexico', 'mexico',       19.433,   -99.133),
            ('Monterrey',        'Mexico', 'mexico',       25.686,  -100.316),
            ('Progreso',         'Mexico', 'mexico',       21.285,   -89.666),
            # Europe
            ('Rotterdam',        'Netherlands', 'europe',  51.906,    4.484),
            ('Amsterdam',        'Netherlands', 'europe',  52.372,    4.896),
            ('Hamburg',          'Germany',     'europe',  53.551,   10.001),
            ('Bremerhaven',      'Germany',     'europe',  53.539,    8.578),
            ('Antwerp',          'Belgium',     'europe',  51.221,    4.404),
            ('Zeebrugge',        'Belgium',     'europe',  51.327,    3.161),
            ('Felixstowe',       'UK',          'europe',  51.964,    1.352),
            ('Southampton',      'UK',          'europe',  50.897,   -1.399),
            ('London',           'UK',          'europe',  51.508,   -0.128),
            ('Liverpool',        'UK',          'europe',  53.408,   -2.978),
            ('Le Havre',         'France',      'europe',  49.494,    0.107),
            ('Marseille',        'France',      'europe',  43.297,    5.381),
            ('Genoa',            'Italy',       'europe',  44.407,    8.934),
            ('Naples',           'Italy',       'europe',  40.852,   14.268),
            ('Gioia Tauro',      'Italy',       'europe',  38.433,   15.901),
            ('Trieste',          'Italy',       'europe',  45.649,   13.777),
            ('Barcelona',        'Spain',       'europe',  41.386,    2.170),
            ('Valencia',         'Spain',       'europe',  39.470,   -0.376),
            ('Algeciras',        'Spain',       'europe',  36.130,   -5.451),
            ('Bilbao',           'Spain',       'europe',  43.263,   -2.935),
            ('Lisbon',           'Portugal',    'europe',  38.717,   -9.143),
            ('Sines',            'Portugal',    'europe',  37.956,   -8.870),
            ('Piraeus',          'Greece',      'europe',  37.943,   23.648),
            ('Thessaloniki',     'Greece',      'europe',  40.640,   22.944),
            ('Istanbul',         'Turkey',      'europe',  41.015,   28.980),
            ('Izmir',            'Turkey',      'europe',  38.419,   27.129),
            ('Gdansk',           'Poland',      'europe',  54.352,   18.647),
            ('Gothenburg',       'Sweden',      'europe',  57.707,   11.967),
            ('Copenhagen',       'Denmark',     'europe',  55.676,   12.568),
            ('Helsinki',         'Finland',     'europe',  60.170,   24.942),
            ('Oslo',             'Norway',      'europe',  59.912,   10.752),
            ('Dublin',           'Ireland',     'europe',  53.349,   -6.260),
            ('Limassol',         'Cyprus',      'europe',  34.675,   33.045),
            ('Riga',             'Latvia',      'europe',  56.946,   24.106),
            ('Tallinn',          'Estonia',     'europe',  59.436,   24.754),
            # Asia Pacific
            ('Shanghai',         'China',       'asia-pacific',  31.224,  121.474),
            ('Shenzhen',         'China',       'asia-pacific',  22.542,  114.054),
            ('Guangzhou',        'China',       'asia-pacific',  23.130,  113.264),
            ('Ningbo',           'China',       'asia-pacific',  29.868,  121.544),
            ('Tianjin',          'China',       'asia-pacific',  39.125,  117.191),
            ('Qingdao',          'China',       'asia-pacific',  36.067,  120.383),
            ('Dalian',           'China',       'asia-pacific',  38.914,  121.614),
            ('Xiamen',           'China',       'asia-pacific',  24.479,  118.090),
            ('Hong Kong',        'China',       'asia-pacific',  22.320,  114.178),
            ('Singapore',        'Singapore',   'asia-pacific',   1.352,  103.820),
            ('Busan',            'South Korea', 'asia-pacific',  35.179,  129.076),
            ('Incheon',          'South Korea', 'asia-pacific',  37.456,  126.706),
            ('Tokyo',            'Japan',       'asia-pacific',  35.690,  139.692),
            ('Yokohama',         'Japan',       'asia-pacific',  35.444,  139.638),
            ('Kobe',             'Japan',       'asia-pacific',  34.690,  135.196),
            ('Osaka',            'Japan',       'asia-pacific',  34.694,  135.502),
            ('Nagoya',           'Japan',       'asia-pacific',  35.181,  136.907),
            ('Kaohsiung',        'Taiwan',      'asia-pacific',  22.616,  120.301),
            ('Keelung',          'Taiwan',      'asia-pacific',  25.127,  121.740),
            ('Taichung',         'Taiwan',      'asia-pacific',  24.148,  120.674),
            ('Laem Chabang',     'Thailand',    'asia-pacific',  13.084,  100.879),
            ('Bangkok',          'Thailand',    'asia-pacific',  13.754,  100.502),
            ('Ho Chi Minh City', 'Vietnam',     'asia-pacific',  10.823,  106.630),
            ('Haiphong',         'Vietnam',     'asia-pacific',  20.844,  106.690),
            ('Hanoi',            'Vietnam',     'asia-pacific',  21.028,  105.854),
            ('Jakarta',          'Indonesia',   'asia-pacific',  -6.208,  106.845),
            ('Surabaya',         'Indonesia',   'asia-pacific',  -7.266,  112.752),
            ('Port Klang',       'Malaysia',    'asia-pacific',   3.000,  101.400),
            ('Penang',           'Malaysia',    'asia-pacific',   5.415,  100.329),
            ('Colombo',          'Sri Lanka',   'asia-pacific',   6.927,   79.861),
            ('Chennai',          'India',       'asia-pacific',  13.083,   80.270),
            ('Mumbai',           'India',       'asia-pacific',  19.076,   72.878),
            ('Nhava Sheva',      'India',       'asia-pacific',  18.949,   72.954),
            ('Mundra',           'India',       'asia-pacific',  22.839,   69.718),
            ('Kolkata',          'India',       'asia-pacific',  22.572,   88.364),
            ('Visakhapatnam',    'India',       'asia-pacific',  17.686,   83.218),
            ('Chittagong',       'Bangladesh',  'asia-pacific',  22.341,   91.832),
            ('Karachi',          'Pakistan',    'asia-pacific',  24.861,   67.010),
            ('Manila',           'Philippines', 'asia-pacific',  14.599,  120.984),
            ('Cebu',             'Philippines', 'asia-pacific',  10.317,  123.891),
            ('Sydney',           'Australia',   'asia-pacific', -33.868,  151.209),
            ('Melbourne',        'Australia',   'asia-pacific', -37.814,  144.963),
            ('Brisbane',         'Australia',   'asia-pacific', -27.471,  153.024),
            ('Fremantle',        'Australia',   'asia-pacific', -32.056,  115.748),
            ('Adelaide',         'Australia',   'asia-pacific', -34.929,  138.600),
            ('Auckland',         'New Zealand', 'asia-pacific', -36.848,  174.763),
            ('Port Moresby',     'Papua New Guinea','asia-pacific', -9.443, 147.180),
            # Middle East
            ('Dubai (Jebel Ali)','UAE',         'middle-east',  25.007,   55.112),
            ('Abu Dhabi',        'UAE',         'middle-east',  24.453,   54.377),
            ('Sharjah',          'UAE',         'middle-east',  25.356,   55.391),
            ('Muscat',           'Oman',        'middle-east',  23.588,   58.380),
            ('Salalah',          'Oman',        'middle-east',  17.019,   54.094),
            ('Jeddah',           'Saudi Arabia','middle-east',  21.543,   39.173),
            ('Dammam',           'Saudi Arabia','middle-east',  26.432,   50.103),
            ('Riyadh',           'Saudi Arabia','middle-east',  24.774,   46.738),
            ('Kuwait City',      'Kuwait',      'middle-east',  29.370,   47.978),
            ('Bahrain',          'Bahrain',     'middle-east',  26.225,   50.586),
            ('Doha',             'Qatar',       'middle-east',  25.286,   51.533),
            ('Beirut',           'Lebanon',     'middle-east',  33.889,   35.495),
            ('Haifa',            'Israel',      'middle-east',  32.819,   34.984),
            ('Ashdod',           'Israel',      'middle-east',  31.804,   34.650),
            ('Alexandria',       'Egypt',       'middle-east',  31.200,   29.919),
            ('Port Said',        'Egypt',       'middle-east',  31.257,   32.284),
            ('Aqaba',            'Jordan',      'middle-east',  29.526,   35.006),
            ('Bandar Abbas',     'Iran',        'middle-east',  27.164,   56.272),
            # Latin America
            ('Santos',           'Brazil',      'latin-america', -23.961,  -46.334),
            ('Itajai',           'Brazil',      'latin-america', -26.908,  -48.661),
            ('Rio de Janeiro',   'Brazil',      'latin-america', -22.907,  -43.173),
            ('Paranagua',        'Brazil',      'latin-america', -25.521,  -48.509),
            ('Salvador',         'Brazil',      'latin-america', -12.972,  -38.512),
            ('Fortaleza',        'Brazil',      'latin-america',  -3.717,  -38.543),
            ('Manaus',           'Brazil',      'latin-america',  -3.119,  -60.022),
            ('Buenos Aires',     'Argentina',   'latin-america', -34.604,  -58.382),
            ('Rosario',          'Argentina',   'latin-america', -32.951,  -60.639),
            ('Callao',           'Peru',        'latin-america', -12.056,  -77.135),
            ('Cartagena',        'Colombia',    'latin-america',  10.391,  -75.480),
            ('Buenaventura',     'Colombia',    'latin-america',   3.883,  -77.030),
            ('Barranquilla',     'Colombia',    'latin-america',  10.964,  -74.797),
            ('Guayaquil',        'Ecuador',     'latin-america',  -2.200,  -79.900),
            ('Colon',            'Panama',      'latin-america',   9.359,  -79.900),
            ('Panama City',      'Panama',      'latin-america',   8.994,  -79.519),
            ('Kingston',         'Jamaica',     'latin-america',  17.997,  -76.794),
            ('Freeport',         'Bahamas',     'latin-america',  26.530,  -78.692),
            ('San Juan',         'Puerto Rico', 'latin-america',  18.466,  -66.108),
            ('Valparaiso',       'Chile',       'latin-america', -33.046,  -71.619),
            ('Valparaiso Port',  'Chile',       'latin-america', -33.046,  -71.619),
            ('Montevideo',       'Uruguay',     'latin-america', -34.901,  -56.165),
            ('Caracas',          'Venezuela',   'latin-america',  10.480,  -66.916),
            ('La Guaira',        'Venezuela',   'latin-america',  10.602,  -66.934),
            # Africa
            ('Durban',           'South Africa','africa', -29.857,  31.029),
            ('Cape Town',        'South Africa','africa', -33.926,  18.424),
            ('Port Elizabeth',   'South Africa','africa', -33.960,  25.613),
            ('Mombasa',          'Kenya',       'africa',  -4.043,  39.668),
            ('Dar es Salaam',    'Tanzania',    'africa',  -6.786,  39.273),
            ('Lagos',            'Nigeria',     'africa',   6.453,   3.396),
            ('Apapa',            'Nigeria',     'africa',   6.446,   3.361),
            ('Tema',             'Ghana',       'africa',   5.639,  -0.016),
            ('Abidjan',          'Ivory Coast', 'africa',   5.359,  -4.008),
            ('Dakar',            'Senegal',     'africa',  14.717, -17.468),
            ('Casablanca',       'Morocco',     'africa',  33.573,  -7.590),
            ('Tanger Med',       'Morocco',     'africa',  35.861,  -5.503),
            ('Djibouti',         'Djibouti',    'africa',  11.825,  42.590),
            ('Maputo',           'Mozambique',  'africa', -25.966,  32.582),
            ('Port Louis',       'Mauritius',   'africa', -20.161,  57.499),
            ('Toamasina',        'Madagascar',  'africa', -18.145,  49.401),
            ('Beira',            'Mozambique',  'africa', -19.843,  34.838),
            ('Luanda',           'Angola',      'africa',  -8.838,  13.234),
            ('Conakry',          'Guinea',      'africa',   9.509, -13.712),
            ('Lome',             'Togo',        'africa',   6.137,   1.222),
            ('Cotonou',          'Benin',       'africa',   6.366,   2.420),
        ]
        seen = set()
        for name, country, zone_key, lat, lng in city_data:
            key = (name, country)
            if key in seen:
                continue
            seen.add(key)
            PortCity.objects.create(name=name, country=country, zone=zones[zone_key], lat=lat, lng=lng)
        self.stdout.write(f'  ✓ Port cities ({len(seen)} cities with coordinates across 12 zones)')

    def _services(self):
        Service.objects.all().delete()
        imgs = [
            'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800&q=80',  # OTR — semi truck on highway
            'https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=800&q=80',  # Drayage — port cranes & containers
            'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80',  # Warehousing — warehouse interior
            'https://images.unsplash.com/photo-1494412519316-5a8d8e11b0e3?w=800&q=80',  # Cross-border — aerial container yard
            'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',     # FTL — truck fleet on road
            'https://images.unsplash.com/photo-1521931961826-fe48677230e5?w=800&q=80',  # Reefer — cargo vessel at sea
            'https://images.unsplash.com/photo-1553413077-190dd305871c?w=800&q=80',     # Heavy-haul — industrial freight
        ]
        data = [
            ('OTR Transportation', 'otr',
             'Long-haul OTR coverage across all 48 U.S. states and Canada. We operate Dry Van, Reefer, and Flatbed equipment — backed by a strong vetted carrier network to guarantee capacity and keep your freight on schedule.',
             'truck',
             ['All 48 U.S. states + Canada', 'Dry Van, Reefer & Flatbed', 'Vetted carrier network', 'Consistent transit times', 'Full truckload dedicated capacity', 'Real-time status updates'], 1),
            ('Drayage Services', 'drayage',
             'Seamless container movement from major ports and rail ramps across the U.S. We handle the short-haul leg between port and warehouse — fast turnaround and reliable chassis management.',
             'anchor',
             ['Major ports & rail ramps', 'Port & rail yard operations', '20\' & 40\' container handling', 'Chassis supply & management', 'Bonded & in-bond moves', 'Same-day & next-day availability'], 2),
            ('Warehousing & Storage', 'warehousing',
             'Flexible warehousing and storage solutions to support your supply chain. Short-term overflow or ongoing distribution support — secure, accessible storage integrated with your transportation operations.',
             'box',
             ['Flexible short & long-term storage', 'Integrated with transportation ops', 'Secure facilities', 'Inventory management support', 'Cross-docking capabilities', 'Nationwide locations'], 3),
            ('Cross-Border US–Canada', 'cross-border',
             'Smooth cross-border transportation between the United States and Canada. Our team manages customs documentation, border compliance, and carrier coordination so your freight crosses without delays.',
             'globe',
             ['Full US–Canada coverage', 'Customs documentation handled', 'Border compliance expertise', 'Vetted cross-border carriers', 'Reefer & hazmat capable', 'On-time cross-border delivery'], 4),
            ('Full Truckload (FTL)', 'ftl',
             'Dedicated capacity for your freight — no co-loading, faster transit, and lower risk of damage. Ideal for time-sensitive or high-value shipments where reliability and speed matter most.',
             'shield',
             ['Dedicated trailer — no co-loading', 'Faster point-to-point transit', 'Ideal for time-critical freight', 'Temperature-controlled options', 'Expedited FTL available', 'Competitive rates nationwide'], 5),
            ('Reefer (Temperature-Controlled)', 'reefer',
             'Temperature-controlled trucking for food, beverages, pharmaceuticals, and other sensitive cargo. We maintain precise temperature ranges from origin to destination, ensuring cold chain integrity throughout.',
             'thermometer',
             ['Precise temperature control', 'Food, pharma & sensitive cargo', 'Cold chain integrity guaranteed', 'Continuous temp monitoring', 'FSMA compliance', 'Nationwide reefer capacity'], 6),
            ('Heavy-Haul & Specialized', 'heavy-haul',
             'Specialized heavy-haul and oversized freight transportation. Our fleet includes Lowboys, Double Drops, RGNs, Extendable Flatbeds, and Multi-Axle Units — with full compliance and permitting support.',
             'zap',
             ['Lowboys, Double Drops, RGNs', 'Extendable Flatbeds & Multi-Axle', 'Oversized & overweight loads', 'Full permit & escort coordination', 'Hazmat transportation capable', 'Project cargo specialists'], 7),
        ]
        for i, (name, slug, desc, icon, features, order) in enumerate(data):
            Service.objects.create(name=name, slug=slug, description=desc, icon_name=icon, features=features, image_url=imgs[i], order=order)
        self.stdout.write('  ✓ Services')

    def _shipment_types(self):
        ShipmentType.objects.all().delete()
        data = [
            ('Dry Van (General Freight)',       'Palletized and non-perishable goods',                'box',       1),
            ('Reefer (Temperature-Controlled)', 'Food, beverages, and cold-chain cargo',              'thermometer',2),
            ('Flatbed',                         'Open freight, machinery, and oversized loads',       'truck',     3),
            ('Full Truckload (FTL)',            'Dedicated, faster transit shipments',                'shield',    4),
            ('Drayage (Port & Rail)',           'Container moves from ports and rail ramps',          'anchor',    5),
            ('Warehousing & Storage',           'Short and long-term storage solutions',              'packages',  6),
            ('Heavy-Haul & Specialized',        'Lowboys, Double Drops, RGNs, Multi-Axle Units',     'zap',       7),
            ('Cross-Border (USA–Canada)',       'Smooth freight coordination across the border',      'globe',     8),
        ]
        for name, desc, icon, order in data:
            ShipmentType.objects.create(name=name, desc=desc, icon=icon, order=order)
        self.stdout.write('  ✓ Shipment types')

    def _why_us_features(self):
        WhyUsFeature.objects.all().delete()
        data = [
            ('truck',      'Vetted & Reliable Carrier Network', 'Every carrier in our network is thoroughly vetted for safety, compliance, and reliability — so your freight moves with providers you can trust.', 1),
            ('bar-chart',  'Competitive & Transparent Pricing', 'No hidden fees. We offer competitive, market-aligned rates with full transparency from quote to delivery across all service modes.', 2),
            ('clock',      '24/7 Operations & Visibility',      'Our operations team is available around the clock with real-time shipment visibility — so you always know where your freight is, day or night.', 3),
            ('headphones', 'Dedicated Account Support',         'You get a dedicated account and operations team who knows your freight requirements and proactively keeps your supply chain running smoothly.', 4),
            ('globe',      '48 States + Canada Coverage',       'Nationwide OTR coverage across all 48 U.S. states plus full cross-border service to Canada — major ports, rail ramps, and distribution hubs.', 5),
            ('shield',     'Service Quality & Compliance',      'Committed to the highest standards of service quality, DOT/FMCSA compliance, and transparency — every load, every lane, every time.', 6),
        ]
        for icon, title, desc, order in data:
            WhyUsFeature.objects.create(icon=icon, title=title, desc=desc, order=order)
        self.stdout.write('  ✓ Why us features')

    def _commitments(self):
        Commitment.objects.all().delete()
        for i, text in enumerate(['On-time pickups and deliveries', 'Proactive communication', 'Flexible capacity solutions', 'Long-term partnership approach'], 1):
            Commitment.objects.create(text=text, order=i)
        self.stdout.write('  ✓ Commitments')

    def _about_highlights(self):
        AboutHighlight.objects.all().delete()
        items = [
            'Operating across all 48 U.S. states',
            'Full coverage across Canada',
            'OTR Transportation — Dry Van, Reefer & Flatbed',
            'Drayage at major ports & rail ramps',
            'Warehousing & storage solutions',
            'Specialized heavy-haul: Lowboys, Double Drops, RGNs',
            'Hazmat & reefer transportation',
            'Strong vetted carrier network',
        ]
        for i, text in enumerate(items, 1):
            AboutHighlight.objects.create(text=text, order=i)
        self.stdout.write('  ✓ About highlights')

    def _industries(self):
        Industry.objects.all().delete()
        for i, name in enumerate(['Retail & E-commerce', 'Manufacturing & Industrial', 'Food & Beverage (Reefer)', 'Automotive & General Freight'], 1):
            Industry.objects.create(name=name, order=i)
        self.stdout.write('  ✓ Industries')

    def _support_channels(self):
        SupportChannel.objects.all().delete()
        data = [
            ('phone',   'Call Us',       '803-666-8368',               'Mon–Fri, standard business hours', 1),
            ('mail',    'Email Support', 'garry@augustusbrokerage.com','Response within 24 hours',          2),
            ('message', 'WhatsApp',      '803-666-8368',               'Quick quotes & load updates',       3),
            ('clock',   '24/7 Dispatch', '803-666-8368',               'Urgent loads always answered',      4),
        ]
        for icon, title, detail, sub, order in data:
            SupportChannel.objects.create(icon=icon, title=title, detail=detail, sub=sub, order=order)
        self.stdout.write('  ✓ Support channels')

    def _offices(self):
        Office.objects.all().delete()
        data = [
            ('Headquarters (USA)',    'United States',            '803-666-8368', 'garry@augustusbrokerage.com', 1),
            ('West Coast Operations', 'LA / Long Beach Port Area','803-666-8368', 'garry@augustusbrokerage.com', 2),
            ('Augustus Logistics UAE','augustomlogisticsuae.com', '+971 4 729 2937','info@augustuslogisticsuae.com',3),
        ]
        for city, address, phone, email, order in data:
            Office.objects.create(city=city, address=address, phone=phone, email=email, order=order)
        self.stdout.write('  ✓ Offices')

    def _career_perks(self):
        CareerPerk.objects.all().delete()
        data = [
            ('Nationwide Reach',   'Work with freight moving across all 48 U.S. states and Canada — high-volume, high-impact operations.', 1),
            ('Vetted Network',     'Join a company built on carrier relationships and compliance — not just brokerage middlemen.', 2),
            ('Multi-Modal Scope',  'Gain experience across OTR, drayage, warehousing, and cross-border freight in a single organisation.', 3),
            ('Growth Opportunity', 'Be part of a fast-growing freight company built on operational excellence and long-term client partnerships.', 4),
        ]
        for title, desc, order in data:
            CareerPerk.objects.create(title=title, desc=desc, order=order)
        self.stdout.write('  ✓ Career perks')

    def _faq(self):
        FaqItem.objects.all().delete()
        data = [
            ('What areas do you cover?',
             'We provide transportation solutions across all 48 contiguous U.S. states and full coverage across Canada, including major ports, rail ramps, and distribution hubs.', 1),
            ('What types of transportation do you specialize in?',
             'We specialise in OTR (Dry Van, Reefer & Flatbed), Drayage (ports & rail ramps), Warehousing & Storage, Cross-Border US–Canada, FTL, Reefer, and Heavy-Haul & Specialized freight.', 2),
            ('Do you have your own trucks or are you a broker?',
             'We operate as a freight brokerage with a strong vetted carrier network. Every carrier is vetted for safety, compliance, and reliability — giving you consistent, trusted capacity.', 3),
            ('Can you handle time-sensitive or urgent shipments?',
             'Yes — we prioritise expedited and time-critical shipments with dedicated carrier capacity and fast response times. Contact our dispatch team directly for urgent loads.', 4),
            ('What makes Augustus Corp different?',
             'Our vetted carrier network, competitive transparent pricing, 24/7 operations visibility, and dedicated account support set us apart. We build long-term partnerships, not one-off transactions.', 5),
            ('What shipment types do you handle?',
             'We handle Dry Van, Reefer, Flatbed, FTL, Drayage (port & rail), Warehousing, Heavy-Haul (Lowboys, Double Drops, RGNs), Hazmat, and Cross-Border USA–Canada shipments.', 6),
            ('Which ports and rail yards do you serve?',
             'We serve major US ports and rail terminals including LA/Long Beach, and key inland intermodal hubs across the country, with full Canada coverage for cross-border moves.', 7),
            ('How do I get a freight quote?',
             'Fill out our online quote form or contact us directly at 803-666-8368 or garry@augustusbrokerage.com. Provide your origin, destination, freight type, and weight — we respond within 24 hours.', 8),
            ('Is there a minimum shipment size?',
             'No minimum — we handle everything from partial loads to full truckloads. Contact us to discuss your specific freight requirements and we\'ll find the right solution.', 9),
            ('Do you handle hazardous materials?',
             'Yes. We ensure fully compliant handling of regulated goods (hazmat) in line with DOT and FMCSA requirements. Please disclose hazmat classification when requesting a quote.', 10),
        ]
        for question, answer, order in data:
            FaqItem.objects.create(question=question, answer=answer, order=order)
        self.stdout.write('  ✓ FAQ items')

    def _testimonials(self):
        Testimonial.objects.all().delete()
        data = [
            ('David Harrington', 'Midwest Manufacturing Co.', 'VP of Supply Chain',
             'Augustus Brokerage handled our OTR moves across 12 states seamlessly. Their vetted carrier network gave us consistent capacity even during peak season when other brokers fell through.', 5,
             'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=100&h=100&fit=crop&crop=face'),
            ('Maria Santos', 'Pacific Fresh Foods', 'Logistics Director',
             'The reefer coordination from Augustus is outstanding. Our produce arrives on time and in perfect condition — cold chain integrity is never compromised.', 5,
             'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&h=100&fit=crop&crop=face'),
            ('James Whitmore', 'Gulf Port Importers', 'CEO',
             'Their drayage team at LA/Long Beach is the most reliable we\'ve worked with. Fast response, no port delays — they\'ve transformed our import operations.', 5,
             'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop&crop=face'),
            ('Angela Park', 'E-Commerce Direct LLC', 'Operations Manager',
             'We switched to Augustus for our cross-border Canada runs and the difference was immediate — better rates, better transit times, and a team that actually picks up the phone.', 5,
             'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=100&h=100&fit=crop&crop=face'),
        ]
        for name, company, position, review, rating, avatar in data:
            Testimonial.objects.create(name=name, company=company, position=position, review=review, rating=rating, avatar_url=avatar)
        self.stdout.write('  ✓ Testimonials')

    def _team(self):
        TeamMember.objects.all().delete()
        data = [
            ('Founder & CEO', 'Founder & Chief Executive Officer',
             'Leads company operations, transport strategy, and business growth initiatives. Brings deep expertise in nationwide freight operations and carrier network development.',
             'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop&crop=face', 1),
            ('Logistics & Operations Manager', 'Logistics & Operations Manager',
             'Oversees transport coordination, load planning, and delivery operations across the national network. Ensures every shipment moves on time.',
             'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop&crop=face', 2),
            ('Carrier Relations Manager', 'Carrier Relations Manager',
             'Builds and maintains relationships with vetted OTR and cross-border carriers. Negotiates rates and manages compliance documentation across the network.',
             'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face', 3),
            ('Client Relations Executive', 'Client Relations Executive',
             'Ensures smooth communication and customer support throughout the shipping process. Your dedicated point of contact from quote to delivery.',
             'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop&crop=face', 4),
        ]
        for name, position, bio, image, order in data:
            TeamMember.objects.create(name=name, position=position, bio=bio, image_url=image, order=order)
        self.stdout.write('  ✓ Team')

    def _blog(self):
        BlogPost.objects.all().delete()
        data = [
            ('OTR vs. Intermodal: Which Mode is Right for Your Freight?',
             'otr-vs-intermodal-guide',
             'Choosing between Over-the-Road trucking and intermodal shipping depends on distance, transit time, and cost priorities. Our experts break down when each mode wins.',
             'Full article content...', 'Augustus Corp', 'Shipping Guide',
             'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=500&fit=crop'),
            ('Understanding Drayage: How Port & Rail Container Moves Work',
             'understanding-drayage-port-rail',
             'Drayage is the critical short-haul leg that connects ports and rail yards to warehouses. Here\'s how Augustus keeps your containers moving without port delays.',
             'Full article content...', 'Augustus Corp', 'Industry Insights',
             'https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=800&h=500&fit=crop'),
            ('Cross-Border Freight: What You Need to Know About US–Canada Shipping',
             'us-canada-cross-border-shipping',
             'Cross-border freight between the US and Canada involves customs documentation, compliance, and the right carrier relationships. Here\'s what shippers need to know.',
             'Full article content...', 'Augustus Corp', 'Operations',
             'https://images.unsplash.com/photo-1521931961826-fe48677230e5?w=800&h=500&fit=crop'),
        ]
        for title, slug, excerpt, content, author, category, image in data:
            BlogPost.objects.create(title=title, slug=slug, excerpt=excerpt, content=content, author=author, category=category, image_url=image)
        self.stdout.write('  ✓ Blog posts')

    def _companies(self):
        Company.objects.all().delete()
        data = [
            (
                'Augustus Brokerage',
                'Trucking & Brokerage Solutions — Reliable · Scalable · On-Time',
                'Augustus Brokerage is a customer-focused trucking and brokerage company providing reliable freight transportation across the United States, Canada, and beyond. With a strong vetted carrier network and commitment to service quality, compliance, and transparency, we keep your supply chain moving.',
                'truck', 'bg-blue-50', 'text-blue-600',
                '2010', 'Vetted carrier network', 'US & Canada', '150+',
                'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
                ['OTR — Dry Van, Reefer & Flatbed', 'Drayage at major ports & rail ramps', 'Warehousing & storage solutions', 'Cross-border US–Canada transportation', 'Vetted and reliable carrier network', 'Competitive and transparent pricing'],
                1,
            ),
            (
                'Augustus Logistics UAE',
                'Middle East Logistics & Distribution',
                'Augustus Logistics UAE (augustuslogisticsuae.com) is our UAE-based specialist subsidiary providing comprehensive freight forwarding, warehousing, and last-mile distribution across the GCC and beyond. Strategically headquartered in Dubai with access to Jebel Ali Port — the region\'s largest container hub.',
                'globe', 'bg-emerald-50', 'text-emerald-600',
                '2015', 'UAE & GCC', '30+', '200+',
                'https://images.unsplash.com/photo-1521931961826-fe48677230e5?w=800&q=80',
                ['UAE & GCC freight forwarding', 'Jebel Ali port operations', 'Bonded warehousing & distribution', 'Door-to-door last-mile delivery', 'Customs brokerage & compliance', 'Cold chain & reefer handling'],
                2,
            ),
        ]
        for name, tagline, desc, icon, bg, ic, founded, fleet, countries, employees, image, highlights, order in data:
            Company.objects.create(name=name, tagline=tagline, description=desc, icon_name=icon, bg_class=bg, icon_class=ic, founded=founded, fleet=fleet, countries=countries, employees=employees, image_url=image, highlights=highlights, order=order)
        self.stdout.write('  ✓ Companies')

    def _shipments(self):
        Shipment.objects.all().delete()
        now = timezone.now()

        s1 = Shipment.objects.create(
            tracking_number='AUGS-2025-001', status='in_transit',
            origin='Chicago, IL', destination='Los Angeles, CA',
            service_type='OTR — Dry Van', weight='42,000 lbs',
            estimated_delivery=date.today() + timedelta(days=3),
            sender_name='Midwest Manufacturing Co.', receiver_name='Pacific Distribution LLC')
        for evt in [
            ('picked_up', 'Chicago, IL',    'Freight picked up from shipper warehouse', now - timedelta(days=2)),
            ('in_transit','Indianapolis, IN','In transit — I-70 West corridor',          now - timedelta(days=1, hours=12)),
            ('in_transit','St. Louis, MO',  'Checkpoint — driver hours reset',           now - timedelta(hours=20)),
            ('in_transit','Oklahoma City, OK','In transit — I-40 West',                  now - timedelta(hours=8)),
        ]:
            TrackingEvent.objects.create(shipment=s1, status=evt[0], location=evt[1], description=evt[2], event_time=evt[3])

        s2 = Shipment.objects.create(
            tracking_number='AUGS-2025-002', status='delivered',
            origin='Atlanta, GA', destination='Dallas, TX',
            service_type='FTL — Reefer', weight='38,000 lbs',
            estimated_delivery=date.today() - timedelta(days=1),
            sender_name='Southeast Fresh Foods', receiver_name='Texas Grocery Chain')
        for evt in [
            ('picked_up', 'Atlanta, GA', 'Reefer unit pre-cooled and loaded',           now - timedelta(days=3)),
            ('in_transit','Birmingham, AL','In transit — I-20 West, temp holding at 34°F', now - timedelta(days=2, hours=18)),
            ('in_transit','Jackson, MS',  'Checkpoint — temp confirmed 34°F',           now - timedelta(days=2)),
            ('in_transit','Shreveport, LA','In transit — I-20 West final leg',          now - timedelta(days=1, hours=8)),
            ('delivered', 'Dallas, TX',   'Delivered and signed for by consignee',       now - timedelta(hours=20)),
        ]:
            TrackingEvent.objects.create(shipment=s2, status=evt[0], location=evt[1], description=evt[2], event_time=evt[3])

        s3 = Shipment.objects.create(
            tracking_number='AUGS-2025-003', status='at_port',
            origin='Seattle, WA', destination='Denver, CO',
            service_type='Drayage + OTR', weight='44,000 lbs',
            estimated_delivery=date.today() + timedelta(days=2),
            sender_name='Pacific Imports Ltd.', receiver_name='Augustus Corp — Denver Warehouse')
        for evt in [
            ('picked_up', 'Port of Seattle',  'Container pulled from port terminal',    now - timedelta(days=1, hours=10)),
            ('at_port',   'Seattle Rail Ramp','Container transferred to rail ramp',      now - timedelta(hours=6)),
        ]:
            TrackingEvent.objects.create(shipment=s3, status=evt[0], location=evt[1], description=evt[2], event_time=evt[3])

        self.stdout.write('  ✓ Shipments & tracking events')

    def _jobs(self):
        Job.objects.all().delete()
        data = [
            ('OTR Truck Driver (CDL-A)', 'Augustus Corp', 'Nationwide (USA)', 'Full-Time', 'Fleet Operations',
             'OTR driver for long-haul dry van routes across all 48 states. Minimum 2 years OTR experience required. Competitive pay, benefits, and home time.'),
            ('Freight Operations Coordinator', 'Augustus Corp', 'USA (Remote/Hybrid)', 'Full-Time', 'Operations',
             'Coordinate daily freight movements across OTR, drayage, and cross-border lanes. Track loads, manage carrier communication, and resolve transit issues proactively.'),
            ('Drayage Dispatcher', 'Augustus Corp', 'Los Angeles, CA', 'Full-Time', 'Operations',
             'Dispatch drayage moves at LA/Long Beach and surrounding rail terminals. Experience with port operations and container tracking required.'),
            ('Business Development Representative', 'Augustus Corp', 'USA (Remote)', 'Full-Time', 'Commercial',
             'Generate new freight accounts across manufacturing, retail, and e-commerce sectors. Cold outreach, follow-up, and RFP experience in trucking or freight forwarding required.'),
            ('Carrier Relations Manager', 'Augustus Corp', 'USA (Remote)', 'Full-Time', 'Operations',
             'Build and maintain relationships with vetted OTR and cross-border carriers. Negotiate rates, manage compliance documentation, and grow the carrier network.'),
            ('Logistics & Admin Officer', 'Augustus Corp', 'USA', 'Full-Time', 'Finance',
             'Support invoicing, freight billing, carrier payments, and internal reporting. Experience with TMS platforms and freight accounting preferred.'),
        ]
        for title, company, location, jtype, dept, desc in data:
            Job.objects.create(title=title, company_name=company, location=location, job_type=jtype, department=dept, description=desc)
        self.stdout.write('  ✓ Jobs')
