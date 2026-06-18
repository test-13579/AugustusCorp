from django.db import models
import json


# ── Singleton site-wide settings ─────────────────────────────────────────────

class SiteSettings(models.Model):
    # ── Brand identity
    company_name  = models.CharField(max_length=100, default='Augustus Corp')
    tagline       = models.CharField(max_length=200, default='Trucking & Brokerage Solutions — Reliable · Scalable · On-Time')
    logo          = models.ImageField(upload_to='branding/', blank=True, null=True,
                                      help_text='Light mode logo (shown on white/light backgrounds)')
    logo_dark     = models.ImageField(upload_to='branding/', blank=True, null=True,
                                      help_text='Dark mode logo (shown on dark backgrounds). Falls back to light logo if not set.')
    logo_alt      = models.CharField(max_length=100, default='Augustus Corp', blank=True,
                                     help_text='Alt text shown if image fails to load')
    favicon       = models.ImageField(upload_to='branding/', blank=True, null=True,
                                      help_text='Favicon (32×32 or 64×64 PNG/ICO)')
    # ── Wordmark (styled name beside logo)
    wordmark_main   = models.CharField(max_length=50, default='AUGUST',
                                       help_text='First part of the brand name (shown in navy)')
    wordmark_accent = models.CharField(max_length=50, default='US',
                                       help_text='Second part shown in accent color (red)')
    wordmark_sub    = models.CharField(max_length=50, default='CORP', blank=True,
                                       help_text='Small text below the wordmark, e.g. CORP or BROKERAGE')
    # ── Brand colors
    primary_color = models.CharField(max_length=7, default='#4A99CC',
                                     help_text='Primary blue — e.g. #4A99CC')
    navy_color    = models.CharField(max_length=7, default='#1A3D5C',
                                     help_text='Dark navy — e.g. #1A3D5C')
    accent_color  = models.CharField(max_length=7, default='#E84231',
                                     help_text='Accent/highlight color — e.g. #E84231')
    # ── Contact & operations
    phone            = models.CharField(max_length=30, default='803-666-8368')
    email            = models.EmailField(default='garry@augustusbrokerage.com')
    address          = models.CharField(max_length=200, default='United States & Canada')
    website          = models.CharField(max_length=100, default='augustustransport.com')
    hours_weekday    = models.CharField(max_length=50, default='8am–6pm ET')
    hours_saturday   = models.CharField(max_length=50, default='9am–2pm ET')
    footer_blurb     = models.TextField(default='Nationwide trucking & freight solutions across all 48 U.S. states and Canada. OTR, Drayage, Warehousing & Cross-Border — backed by a vetted carrier network.')
    meta_description = models.TextField(default='Augustus Corp — End-to-end logistics solutions. Reliable, scalable, on-time freight across the US and Canada.')
    # ── Site images (uploaded via admin — no external URLs needed)
    hero_poster    = models.ImageField(upload_to='site/', blank=True, null=True,
                                       help_text='Fallback image shown if the hero video fails to load')
    about_image    = models.ImageField(upload_to='site/', blank=True, null=True,
                                       help_text='Main photo used in the About section (home & about pages)')
    about_image_2  = models.ImageField(upload_to='site/', blank=True, null=True,
                                       help_text='Small secondary photo in the About section on the home page')
    cta_bg         = models.ImageField(upload_to='site/', blank=True, null=True,
                                       help_text='Background photo for the CTA / call-to-action banner')
    career_bg      = models.ImageField(upload_to='site/', blank=True, null=True,
                                       help_text='Background photo for the Careers page header')
    contact_bg     = models.ImageField(upload_to='site/', blank=True, null=True,
                                       help_text='Background photo for the Contact page map banner')
    gallery_1      = models.ImageField(upload_to='site/gallery/', blank=True, null=True,
                                       help_text='Gallery image 1 (top-left in Why Us section)')
    gallery_2      = models.ImageField(upload_to='site/gallery/', blank=True, null=True,
                                       help_text='Gallery image 2 (bottom-left in Why Us section)')
    gallery_3      = models.ImageField(upload_to='site/gallery/', blank=True, null=True,
                                       help_text='Gallery image 3 (top-right in Why Us section)')
    gallery_4      = models.ImageField(upload_to='site/gallery/', blank=True, null=True,
                                       help_text='Gallery image 4 (bottom-right in Why Us section)')
    # ── Integrations
    google_maps_api_key = models.CharField(max_length=200, blank=True, default='',
                                            help_text='Google Maps API key (enable Distance Matrix API + Maps JavaScript API in Google Cloud Console)')
    # ── Social media
    social_facebook  = models.URLField(max_length=200, blank=True, default='',
                                       help_text='Facebook page URL (leave blank to hide icon)')
    social_linkedin  = models.URLField(max_length=200, blank=True, default='',
                                       help_text='LinkedIn company/profile URL (leave blank to hide icon)')
    social_twitter   = models.URLField(max_length=200, blank=True, default='',
                                       help_text='Twitter / X profile URL (leave blank to hide icon)')
    social_reddit    = models.URLField(max_length=200, blank=True, default='',
                                       help_text='Reddit community URL (leave blank to hide icon)')
    social_instagram = models.URLField(max_length=200, blank=True, default='',
                                       help_text='Instagram profile URL (leave blank to hide icon)')
    social_youtube   = models.URLField(max_length=200, blank=True, default='',
                                       help_text='YouTube channel URL (leave blank to hide icon)')

    class Meta:
        verbose_name        = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # prevent deletion of the singleton

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f'Site Settings — {self.company_name}'


# ── Content blocks ────────────────────────────────────────────────────────────

class FaqItem(models.Model):
    question = models.CharField(max_length=300)
    answer   = models.TextField()
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'FAQ Item'
        verbose_name_plural = 'FAQ Items'

    def __str__(self):
        return self.question


class Commitment(models.Model):
    text  = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Industry(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True,
                                   help_text='Short description shown on the card (2–3 sentences)')
    icon_name   = models.CharField(max_length=50, blank=True,
                                   help_text='SVG icon key: car, chip, cross, gear, bag, plane, bolt, snowflake')
    logo        = models.ImageField(upload_to='industries/logos/', blank=True, null=True,
                                    help_text='Custom icon/logo for the card (overrides SVG icon if set)')
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Industry'
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name


class AboutHighlight(models.Model):
    text  = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'About Highlight'
        verbose_name_plural = 'About Highlights'

    def __str__(self):
        return self.text


class WhyUsFeature(models.Model):
    icon  = models.CharField(max_length=50, help_text='Icon name (e.g. truck, globe, shield)')
    title = models.CharField(max_length=100)
    desc  = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Why Us Feature'
        verbose_name_plural = 'Why Us Features'

    def __str__(self):
        return self.title


class ShipmentType(models.Model):
    name  = models.CharField(max_length=100)
    desc  = models.CharField(max_length=200)
    icon  = models.CharField(max_length=50, help_text='Icon name (e.g. box, truck, anchor)')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Shipment Type'
        verbose_name_plural = 'Shipment Types'

    def __str__(self):
        return self.name


class SupportChannel(models.Model):
    icon   = models.CharField(max_length=50)
    title  = models.CharField(max_length=100)
    detail = models.CharField(max_length=200)
    sub    = models.CharField(max_length=200)
    order  = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Support Channel'
        verbose_name_plural = 'Support Channels'

    def __str__(self):
        return self.title


class Office(models.Model):
    city    = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone   = models.CharField(max_length=30)
    email   = models.EmailField()
    order   = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.city


class CareerPerk(models.Model):
    title = models.CharField(max_length=100)
    desc  = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Career Perk'
        verbose_name_plural = 'Career Perks'

    def __str__(self):
        return self.title


class Service(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.TextField()
    icon_name   = models.CharField(max_length=50)
    features    = models.JSONField(default=list)
    image       = models.ImageField(upload_to='services/', blank=True, null=True)
    logo        = models.ImageField(upload_to='services/logos/', blank=True, null=True,
                                    help_text='Service icon/logo shown on cards (overrides SVG icon if set)')
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name      = models.CharField(max_length=100)
    company   = models.CharField(max_length=100)
    position  = models.CharField(max_length=100)
    review    = models.TextField()
    rating    = models.PositiveSmallIntegerField(default=5)
    avatar     = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} — {self.company}"

    @property
    def stars(self):
        return range(self.rating)

    @property
    def empty_stars(self):
        return range(5 - self.rating)


class TeamMember(models.Model):
    name      = models.CharField(max_length=100)
    position  = models.CharField(max_length=100)
    bio       = models.TextField()
    image     = models.ImageField(upload_to='team/', blank=True, null=True)
    order     = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    excerpt      = models.TextField()
    content      = models.TextField()
    author       = models.CharField(max_length=100)
    category     = models.CharField(max_length=60)
    image        = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Company(models.Model):
    name        = models.CharField(max_length=100)
    tagline     = models.CharField(max_length=100)
    description = models.TextField()
    icon_name   = models.CharField(max_length=50)
    bg_class    = models.CharField(max_length=60, default='bg-blue-50')
    icon_class  = models.CharField(max_length=60, default='text-blue-600')
    founded     = models.CharField(max_length=20)
    fleet       = models.CharField(max_length=50)
    countries   = models.CharField(max_length=20)
    employees   = models.CharField(max_length=20)
    image           = models.ImageField(upload_to='companies/', blank=True, null=True)
    logo            = models.ImageField(upload_to='companies/logos/', blank=True, null=True,
                                        help_text='Company logo shown as the small icon in the card header')
    highlights      = models.JSONField(default=list)
    show_calculator = models.BooleanField(default=True,
                                          help_text='Show the trucking cost calculator for this company on the Companies page')
    order           = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('picked_up',        'Cargo Received'),
        ('in_transit',       'Vessel In Transit'),
        ('customs',          'At Customs / Port'),
        ('at_port',          'At Destination Port'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered',        'Delivered'),
    ]
    tracking_number    = models.CharField(max_length=30, unique=True)
    status             = models.CharField(max_length=30, choices=STATUS_CHOICES, default='picked_up')
    origin             = models.CharField(max_length=100)
    destination        = models.CharField(max_length=100)
    service_type       = models.CharField(max_length=100)
    weight             = models.CharField(max_length=30, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    sender_name        = models.CharField(max_length=100, blank=True)
    receiver_name      = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.tracking_number

    def get_status_display_class(self):
        colours = {
            'picked_up': 'bg-blue-500',
            'in_transit': 'bg-navy-700',
            'customs': 'bg-yellow-500',
            'at_port': 'bg-cyan-600',
            'out_for_delivery': 'bg-purple-500',
            'delivered': 'bg-green-500',
        }
        return colours.get(self.status, 'bg-gray-500')


class TrackingEvent(models.Model):
    shipment   = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='events')
    status     = models.CharField(max_length=30)
    location   = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    event_time = models.DateTimeField()

    class Meta:
        ordering = ['-event_time']

    def __str__(self):
        return f"{self.shipment.tracking_number} — {self.description}"


class Job(models.Model):
    TYPE_CHOICES = [('Full-Time', 'Full-Time'), ('Sea-Based', 'Sea-Based'), ('Contract', 'Contract')]
    title        = models.CharField(max_length=150)
    company_name = models.CharField(max_length=100)
    location     = models.CharField(max_length=100)
    job_type     = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Full-Time')
    department   = models.CharField(max_length=80)
    description  = models.TextField()
    posted_date  = models.DateField(auto_now_add=True)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['-posted_date']

    def __str__(self):
        return f"{self.title} — {self.location}"


class JobApplication(models.Model):
    job        = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    phone      = models.CharField(max_length=30, blank=True)
    cover_note = models.TextField(blank=True)
    cv_file    = models.FileField(upload_to='applications/cv/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.name} → {self.job.title}"


class Quote(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    company      = models.CharField(max_length=100, blank=True)
    service_type = models.CharField(max_length=100)
    origin       = models.CharField(max_length=100)
    destination  = models.CharField(max_length=100)
    weight       = models.CharField(max_length=50, blank=True)
    dimensions   = models.CharField(max_length=100, blank=True)
    message      = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status       = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Quote #{self.pk} — {self.name} ({self.service_type})"


class Contact(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    subject      = models.CharField(max_length=200)
    message      = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} — {self.subject}"


# ── Freight rate calculator ───────────────────────────────────────────────────

class CalcService(models.Model):
    name       = models.CharField(max_length=100, help_text='e.g. Full Truckload (FTL)')
    key        = models.SlugField(unique=True, help_text='Unique identifier, e.g. ftl')
    base_rate  = models.DecimalField(max_digits=10, decimal_places=2, help_text='Base rate in USD')
    unit_label = models.CharField(max_length=50, default='per load', help_text='e.g. per load, per pallet')
    is_active  = models.BooleanField(default=True)
    order      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Calculator Service'
        verbose_name_plural = 'Calculator Services'

    def __str__(self):
        return f'{self.name} — ${self.base_rate}'


class CalcZone(models.Model):
    name  = models.CharField(max_length=100, help_text='e.g. West Coast USA')
    key   = models.SlugField(unique=True, help_text='e.g. west-coast-usa')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Rate Zone'
        verbose_name_plural = 'Rate Zones'

    def __str__(self):
        return self.name


class CalcRoute(models.Model):
    origin_zone  = models.ForeignKey(CalcZone, on_delete=models.CASCADE, related_name='outbound_routes')
    dest_zone    = models.ForeignKey(CalcZone, on_delete=models.CASCADE, related_name='inbound_routes')
    multiplier   = models.DecimalField(max_digits=6, decimal_places=3, default=1.000,
                                       help_text='Rate multiplier applied to base rate')
    transit_days = models.CharField(max_length=30, default='3–5',
                                    help_text='e.g. 3–5 or Contact us for international')

    class Meta:
        unique_together     = ['origin_zone', 'dest_zone']
        verbose_name        = 'Route Rate'
        verbose_name_plural = 'Route Rates'
        ordering            = ['origin_zone__order', 'dest_zone__order']

    def __str__(self):
        return f'{self.origin_zone} → {self.dest_zone} (×{self.multiplier}, {self.transit_days} days)'


class PortCity(models.Model):
    name      = models.CharField(max_length=100)
    country   = models.CharField(max_length=100)
    zone      = models.ForeignKey(CalcZone, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='cities')
    lat       = models.FloatField(null=True, blank=True, help_text='Latitude (e.g. 34.052)')
    lng       = models.FloatField(null=True, blank=True, help_text='Longitude (e.g. -118.244)')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering            = ['country', 'name']
        verbose_name        = 'Port / City'
        verbose_name_plural = 'Port Cities'

    def __str__(self):
        return f'{self.name}, {self.country}'


# ── Trucking cost calculator ──────────────────────────────────────────────────

class TruckType(models.Model):
    name          = models.CharField(max_length=100, help_text='e.g. Dry Van 53\'')
    key           = models.SlugField(unique=True)
    description   = models.CharField(max_length=200, blank=True)
    capacity      = models.CharField(max_length=100, blank=True, help_text='e.g. 44,000 lbs / 2,700 cu ft')
    rate_per_mile = models.DecimalField(max_digits=6, decimal_places=2,
                                        help_text='Base rate in USD per mile')
    min_charge    = models.DecimalField(max_digits=8, decimal_places=2,
                                        help_text='Minimum charge in USD')
    fuel_surcharge_pct = models.DecimalField(max_digits=5, decimal_places=2, default=25.00,
                                              help_text='Fuel surcharge percentage (e.g. 25 = 25%)')
    is_active     = models.BooleanField(default=True)
    order         = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Vessel Size'
        verbose_name_plural = 'Vessel Sizes'

    def __str__(self):
        return f'{self.name} — ${self.rate_per_mile}/mile'


class CargoType(models.Model):
    name        = models.CharField(max_length=100, help_text='e.g. General Freight')
    key         = models.SlugField(unique=True)
    description = models.CharField(max_length=200, blank=True)
    multiplier  = models.DecimalField(max_digits=4, decimal_places=2, default=1.00,
                                      help_text='Cost multiplier (e.g. 1.5 = 50% surcharge)')
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Cargo Type'
        verbose_name_plural = 'Cargo Types'

    def __str__(self):
        return f'{self.name} (×{self.multiplier})'


# ── Navigation links ──────────────────────────────────────────────────────────

class NavLink(models.Model):
    label     = models.CharField(max_length=60, help_text='Text shown in the navigation bar')
    url       = models.CharField(max_length=200, help_text='Absolute path or full URL, e.g. /about/ or https://…')
    order     = models.PositiveIntegerField(default=0, help_text='Lower number = appears first')
    is_active = models.BooleanField(default=True, help_text='Uncheck to hide from nav without deleting')

    class Meta:
        ordering            = ['order']
        verbose_name        = 'Nav Link'
        verbose_name_plural = 'Nav Links'

    def __str__(self):
        return f'{self.label} → {self.url}'
