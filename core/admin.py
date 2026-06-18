from django.contrib import admin
from .models import (
    Service, Testimonial, TeamMember, BlogPost,
    Company, Shipment, TrackingEvent, Job, JobApplication, Quote, Contact,
    SiteSettings, FaqItem, Commitment, Industry, AboutHighlight,
    WhyUsFeature, ShipmentType, SupportChannel, Office, CareerPerk,
    CalcService, CalcZone, CalcRoute, PortCity,
    TruckType, CargoType, NavLink,
)

admin.site.site_header  = "Augustus Corp — Admin"
admin.site.site_title   = "Augustus Corp Admin"
admin.site.index_title  = "Management Dashboard  ·  📖 Admin Guide → /admin-guide/"


# ── Site Settings ─────────────────────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Logo', {
            'description': 'Upload separate logos for light and dark mode. If no dark logo is set, the light logo is used in both modes.',
            'fields': ('logo', 'logo_dark', 'logo_alt'),
        }),
        ('Favicon (Title Bar Icon)', {
            'description': 'The small icon shown in the browser tab and bookmarks. Upload a square PNG or ICO file — 32×32 px minimum, 512×512 px recommended.',
            'fields': ('favicon',),
        }),
        ('Identity', {
            'fields': ('company_name', 'tagline'),
        }),
        ('Wordmark (styled name beside logo)', {
            'description': 'Controls the typographic brand name shown next to the logo in the header.',
            'fields': ('wordmark_main', 'wordmark_accent', 'wordmark_sub'),
        }),
        ('Brand Colors', {
            'description': 'Enter hex color codes (e.g. #4A99CC). Changes apply site-wide instantly.',
            'fields': ('primary_color', 'navy_color', 'accent_color'),
        }),
        ('Website & SEO', {
            'fields': ('website', 'meta_description', 'footer_blurb'),
        }),
        ('Contact', {
            'fields': ('phone', 'email', 'address'),
        }),
        ('Business Hours', {
            'fields': ('hours_weekday', 'hours_saturday'),
        }),
        ('Site Images — Hero & About', {
            'description': 'Upload photos used on the home page. No external URLs needed — all served from your own server.',
            'fields': ('hero_poster', 'about_image', 'about_image_2', 'cta_bg'),
        }),
        ('Site Images — Inner Pages', {
            'description': 'Background photos for the Careers and Contact pages.',
            'fields': ('career_bg', 'contact_bg'),
        }),
        ('Site Images — Gallery (Why Us section)', {
            'description': 'Four photos shown in the 2×2 collage on the home page.',
            'fields': ('gallery_1', 'gallery_2', 'gallery_3', 'gallery_4'),
        }),
        ('Integrations', {
            'description': 'Third-party API keys. Get a Google Maps API key from console.cloud.google.com — enable Distance Matrix API and Maps JavaScript API.',
            'fields': ('google_maps_api_key',),
        }),
        ('Social Media', {
            'description': 'Enter the full URL for each social profile (e.g. https://www.linkedin.com/company/your-company). Leave blank to hide the icon from the header and footer.',
            'fields': ('social_facebook', 'social_linkedin', 'social_twitter', 'social_reddit', 'social_instagram', 'social_youtube'),
        }),
    )

    def has_add_permission(self, _request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, _request, _obj=None):
        return False


# ── Navigation Links ──────────────────────────────────────────────────────────

@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display  = ['label', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering      = ['order']
    help_text     = 'Drag rows or edit the Order field to reorder the navigation bar. Uncheck Is Active to hide a link without deleting it.'


# ── Services ──────────────────────────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display        = ['name', 'slug', 'icon_name', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering            = ['order']
    fields              = ['name', 'slug', 'description', 'icon_name', 'logo', 'image', 'features', 'order']


# ── Shipment Types ────────────────────────────────────────────────────────────

@admin.register(ShipmentType)
class ShipmentTypeAdmin(admin.ModelAdmin):
    list_display  = ['name', 'desc', 'icon', 'order']
    list_editable = ['order']
    ordering      = ['order']


# ── Why Us Features ───────────────────────────────────────────────────────────

@admin.register(WhyUsFeature)
class WhyUsFeatureAdmin(admin.ModelAdmin):
    list_display  = ['title', 'icon', 'order']
    list_editable = ['order']
    ordering      = ['order']


# ── FAQ ───────────────────────────────────────────────────────────────────────

@admin.register(FaqItem)
class FaqItemAdmin(admin.ModelAdmin):
    list_display  = ['question', 'order']
    list_editable = ['order']
    ordering      = ['order']
    search_fields = ['question', 'answer']


# ── About ─────────────────────────────────────────────────────────────────────

@admin.register(Commitment)
class CommitmentAdmin(admin.ModelAdmin):
    list_display  = ['text', 'order']
    list_editable = ['order']
    ordering      = ['order']


@admin.register(AboutHighlight)
class AboutHighlightAdmin(admin.ModelAdmin):
    list_display  = ['text', 'order']
    list_editable = ['order']
    ordering      = ['order']


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'icon_name', 'order']
    list_editable = ['order']
    ordering      = ['order']
    fields        = ['name', 'slug', 'description', 'icon_name', 'logo', 'order']


# ── Support ───────────────────────────────────────────────────────────────────

@admin.register(SupportChannel)
class SupportChannelAdmin(admin.ModelAdmin):
    list_display  = ['title', 'detail', 'sub', 'order']
    list_editable = ['order']
    ordering      = ['order']


# ── Offices ───────────────────────────────────────────────────────────────────

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display  = ['city', 'address', 'phone', 'email', 'order']
    list_editable = ['order']
    ordering      = ['order']


# ── Team ──────────────────────────────────────────────────────────────────────

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'order']
    ordering     = ['order']
    fields       = ['name', 'position', 'bio', 'image', 'order']


# ── Testimonials ──────────────────────────────────────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'position', 'rating']
    fields       = ['name', 'company', 'position', 'review', 'rating', 'avatar']


# ── Companies ─────────────────────────────────────────────────────────────────

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'tagline', 'founded', 'show_calculator', 'order']
    ordering     = ['order']
    fields       = ['name', 'tagline', 'description', 'logo', 'image', 'icon_name', 'bg_class', 'icon_class', 'founded', 'fleet', 'countries', 'employees', 'highlights', 'show_calculator', 'order']


# ── Blog ──────────────────────────────────────────────────────────────────────

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display        = ['title', 'author', 'category', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    list_filter         = ['category']
    search_fields       = ['title', 'author']
    fields              = ['title', 'slug', 'image', 'excerpt', 'content', 'author', 'category']


# ── Shipments & Tracking ──────────────────────────────────────────────────────

class TrackingEventInline(admin.TabularInline):
    model   = TrackingEvent
    extra   = 1
    ordering = ['event_time']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display  = ['tracking_number', 'status', 'origin', 'destination', 'service_type']
    list_filter   = ['status', 'service_type']
    search_fields = ['tracking_number', 'sender_name', 'receiver_name']
    inlines       = [TrackingEventInline]


# ── Jobs ──────────────────────────────────────────────────────────────────────

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ['title', 'company_name', 'location', 'job_type', 'department', 'is_active', 'posted_date']
    list_filter   = ['job_type', 'department', 'is_active']
    search_fields = ['title', 'location']
    list_editable = ['is_active']


# ── Job Applications ──────────────────────────────────────────────────────────

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'phone', 'job', 'applied_at', 'cv_file']
    list_filter   = ['job', 'applied_at']
    search_fields = ['name', 'email', 'job__title']
    readonly_fields = ['applied_at']


# ── Career Perks ──────────────────────────────────────────────────────────────

@admin.register(CareerPerk)
class CareerPerkAdmin(admin.ModelAdmin):
    list_display  = ['title', 'order']
    list_editable = ['order']
    ordering      = ['order']


# ── Freight Rate Calculator ───────────────────────────────────────────────────

@admin.register(CalcService)
class CalcServiceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'key', 'base_rate', 'unit_label', 'is_active', 'order']
    list_editable = ['base_rate', 'is_active', 'order']
    ordering      = ['order']


@admin.register(CalcZone)
class CalcZoneAdmin(admin.ModelAdmin):
    list_display  = ['name', 'key', 'order']
    list_editable = ['order']
    ordering      = ['order']


@admin.register(CalcRoute)
class CalcRouteAdmin(admin.ModelAdmin):
    list_display  = ['origin_zone', 'dest_zone', 'multiplier', 'transit_days']
    list_editable = ['multiplier', 'transit_days']
    list_filter   = ['origin_zone', 'dest_zone']
    ordering      = ['origin_zone__order', 'dest_zone__order']


@admin.register(PortCity)
class PortCityAdmin(admin.ModelAdmin):
    list_display  = ['name', 'country', 'zone', 'lat', 'lng', 'is_active']
    list_editable = ['zone', 'lat', 'lng', 'is_active']
    list_filter   = ['zone', 'country', 'is_active']
    search_fields = ['name', 'country']
    ordering      = ['country', 'name']


@admin.register(TruckType)
class TruckTypeAdmin(admin.ModelAdmin):
    list_display  = ['name', 'capacity', 'rate_per_mile', 'min_charge', 'fuel_surcharge_pct', 'is_active', 'order']
    list_editable = ['rate_per_mile', 'min_charge', 'fuel_surcharge_pct', 'is_active', 'order']
    ordering      = ['order']
    verbose_name  = 'Vehicle Size'


@admin.register(CargoType)
class CargoTypeAdmin(admin.ModelAdmin):
    list_display  = ['name', 'description', 'multiplier', 'is_active', 'order']
    list_editable = ['multiplier', 'is_active', 'order']
    ordering      = ['order']


# ── Quotes & Contacts ─────────────────────────────────────────────────────────

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display    = ['name', 'email', 'service_type', 'origin', 'destination', 'status', 'submitted_at']
    list_filter     = ['status', 'service_type']
    search_fields   = ['name', 'email']
    readonly_fields = ['submitted_at']
    list_editable   = ['status']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display    = ['name', 'email', 'subject', 'is_read', 'submitted_at']
    list_filter     = ['is_read']
    list_editable   = ['is_read']
    readonly_fields = ['submitted_at']
    search_fields   = ['name', 'email', 'subject']
