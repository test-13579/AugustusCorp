import json
import math
import urllib.request
import urllib.error
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import (
    Service, Testimonial, TeamMember, BlogPost, Company, Shipment, Job,
    JobApplication, Quote, Contact, FaqItem, Commitment, Industry, AboutHighlight,
    WhyUsFeature, ShipmentType, SupportChannel, Office, CareerPerk,
    CalcService, CalcZone, CalcRoute, PortCity, TruckType, CargoType,
)
from .forms import TrackingForm, QuoteForm, ContactForm


# ── Calculator utilities ──────────────────────────────────────────────────────

def _haversine(lat1, lng1, lat2, lng2):
    R = 3958.8
    r = math.pi / 180
    dLat = (lat2 - lat1) * r
    dLng = (lng2 - lng1) * r
    a = math.sin(dLat/2)**2 + math.cos(lat1*r) * math.cos(lat2*r) * math.sin(dLng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def _fmt_duration(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    if h < 24:
        return f'{h}h {m}m'
    d = h // 24
    rh = h % 24
    return f'{d} days {rh}h' if rh else f'{d} days'

def _decode_polyline(encoded):
    idx = lat = lng = 0
    coords = []
    while idx < len(encoded):
        b = shift = result = 0
        while True:
            b = ord(encoded[idx]) - 63
            idx += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lat += ~(result >> 1) if result & 1 else result >> 1
        shift = result = 0
        while True:
            b = ord(encoded[idx]) - 63
            idx += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lng += ~(result >> 1) if result & 1 else result >> 1
        coords.append([lat / 1e5, lng / 1e5])
    return coords

def _osrm_route(orig_lat, orig_lng, dest_lat, dest_lng):
    """Call OSRM public API for driving route. Returns dict or None."""
    url = (f'https://router.project-osrm.org/route/v1/driving/'
           f'{orig_lng},{orig_lat};{dest_lng},{dest_lat}'
           f'?overview=full&geometries=polyline')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AugustusCorp-Calculator/1.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        if data.get('code') == 'Ok' and data.get('routes'):
            rt = data['routes'][0]
            return {
                'miles':    round(rt['distance'] / 1609.344),
                'duration': _fmt_duration(rt['duration']),
                'coords':   _decode_polyline(rt['geometry']),
            }
    except Exception:
        pass
    return None


HERO_STATS = [('3', 'Operating Companies'), ('3', 'Countries'), ('100+', 'Clients Served'), ('24/7', 'Operations')]

CTA_STATS = [
    ('3', 'Operating Companies'), ('3', 'Countries'),
    ('100+', 'Clients Served'), ('24/7', 'Operations'),
]

TRUST_LABELS = ['Response within 24h', 'No-obligation quote', 'Competitive nationwide rates']


def _companies_with_stats(qs):
    companies = list(qs)
    for co in companies:
        co.stat_pairs = [('Founded', co.founded), ('Fleet', co.fleet), ('Countries', co.countries)]
    return companies


def _companies_with_full_stats(qs):
    companies = list(qs)
    for co in companies:
        co.stat_pairs = [('Founded', co.founded), ('Fleet', co.fleet), ('Countries', co.countries), ('Staff', co.employees)]
    return companies


# ── Views ─────────────────────────────────────────────────────────────────────

def _calc_json():
    """Build minimal JSON for the frontend — NO rates or formulas exposed."""
    # Only names for dropdowns (rates/multipliers stay server-side)
    trucks = {t.key: {'name': t.name, 'capacity': t.capacity}
              for t in TruckType.objects.filter(is_active=True)}
    cargos = {c.key: {'name': c.name}
              for c in CargoType.objects.filter(is_active=True)}
    # City names only for autocomplete datalist
    city_names = sorted(
        f'{c.name}, {c.country}'
        for c in PortCity.objects.filter(is_active=True, lat__isnull=False)
    )
    return json.dumps(trucks), json.dumps(cargos), json.dumps(city_names)


class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html', {
            'services':         Service.objects.all()[:6],
            'industries':       Industry.objects.all(),
            'testimonials':     Testimonial.objects.all(),
            'companies':        _companies_with_stats(Company.objects.all()),
            'posts':            BlogPost.objects.all()[:3],
            'hero_stats':         HERO_STATS,
            'cta_stats':          CTA_STATS,
            'about_highlights':   AboutHighlight.objects.all(),
            'why_us_features':    WhyUsFeature.objects.all(),
        })


class AboutView(View):
    def get(self, request):
        return render(request, 'pages/about.html', {
            'team':             TeamMember.objects.all(),
            'commitments':      Commitment.objects.all(),
            'industries':       Industry.objects.values_list('name', flat=True),
            'about_highlights': AboutHighlight.objects.all(),
        })


class ServicesView(View):
    def get(self, request):
        return render(request, 'pages/services.html', {
            'services':       Service.objects.all(),
            'shipment_types': ShipmentType.objects.all(),
            'industries':     Industry.objects.all(),
        })


class CompaniesView(View):
    def get(self, request):
        trucks_json, cargos_json, cities_json = _calc_json()
        return render(request, 'pages/companies.html', {
            'companies':         _companies_with_full_stats(Company.objects.all()),
            'group_stats':       [('3', 'Operating Companies'), ('3', 'Countries'), ('100+', 'Clients Served'), ('24/7', 'Operations')],
            'calc_trucks':       TruckType.objects.filter(is_active=True),
            'calc_cargos':       CargoType.objects.filter(is_active=True),
            'calc_trucks_json':  trucks_json,
            'calc_cargos_json':  cargos_json,
            'calc_cities_json':  cities_json,
        })


class TrackView(View):
    def get(self, request):
        q      = request.GET.get('q', '').strip()
        result = None
        error  = None
        if q:
            try:
                result = Shipment.objects.prefetch_related('events').get(tracking_number=q.upper())
            except Shipment.DoesNotExist:
                error = f'No shipment found for "{q}". Try: AUGS-2025-001, AUGS-2025-002, or AUGS-2025-003'
        result_details = []
        if result:
            result_details = [
                ('Origin',            result.origin),
                ('Destination',       result.destination),
                ('Cargo Weight',      result.weight or '—'),
                ('Est. Delivery',     result.estimated_delivery.strftime('%b %d, %Y') if result.estimated_delivery else '—'),
            ]
        return render(request, 'pages/track.html', {
            'form':           TrackingForm(initial={'tracking_number': q}),
            'result':         result,
            'error':          error,
            'result_details': result_details,
            'status_guide': [
                ('bg-blue-500',   'Cargo Received',      'Cargo collected and at our facility.'),
                ('bg-navy-700',   'In Transit',          'Freight is en route to destination.'),
                ('bg-yellow-500', 'At Customs / Port',   'Cargo undergoing customs or port clearance.'),
                ('bg-cyan-600',   'At Destination',      'Cargo arrived, ready for collection.'),
                ('bg-green-500',  'Delivered',           'Cargo delivered and signed for.'),
            ],
        })

    def post(self, request):
        form = TrackingForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['tracking_number'].strip().upper()
            return redirect(f'/track/?q={num}')
        return redirect('/track/')


class QuoteView(View):
    def _ctx(self, form, success=False, ref=None):
        return {'form': form, 'success': success, 'ref': ref, 'trust_labels': TRUST_LABELS}

    def get(self, request):
        return render(request, 'pages/quote.html', self._ctx(QuoteForm()))

    def post(self, request):
        form = QuoteForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            q = Quote.objects.create(
                name=d['name'], email=d['email'], phone=d.get('phone', ''),
                company=d.get('company', ''), service_type=d['service_type'],
                origin=d['origin'], destination=d['destination'],
                weight=d.get('weight', ''), dimensions=d.get('dimensions', ''),
                message=d.get('message', ''),
            )
            return render(request, 'pages/quote.html', self._ctx(QuoteForm(), success=True, ref=f"QT-{str(q.pk).zfill(5)}"))
        return render(request, 'pages/quote.html', self._ctx(form))


class ContactView(View):
    def _ctx(self, form, success=False):
        return {
            'form':       form,
            'success':    success,
            'offices':    Office.objects.all(),
            'info_cards': [
                {'icon': 'phone', 'title': 'Call Us',      'line1': '803-666-8368',               'line2': 'Mon–Fri, 8am–6pm ET'},
                {'icon': 'mail',  'title': 'Email Us',     'line1': 'garry@augustusbrokerage.com','line2': 'Response within 24 hours'},
                {'icon': 'map',   'title': 'Coverage',     'line1': 'United States & Canada',     'line2': 'Nationwide + Cross-Border'},
                {'icon': 'clock', 'title': '24/7 Dispatch','line1': '803-666-8368',               'line2': 'Always available for urgent loads'},
            ],
        }

    def get(self, request):
        return render(request, 'pages/contact.html', self._ctx(ContactForm()))

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            Contact.objects.create(
                name=d['name'], email=d['email'], phone=d.get('phone', ''),
                subject=d['subject'], message=d['message'],
            )
            return render(request, 'pages/contact.html', self._ctx(ContactForm(), success=True))
        return render(request, 'pages/contact.html', self._ctx(form))


class BlogView(View):
    def get(self, request):
        category   = request.GET.get('cat', '')
        posts      = BlogPost.objects.all()
        if category:
            posts = posts.filter(category=category)
        categories = BlogPost.objects.values_list('category', flat=True).distinct()
        return render(request, 'pages/blog.html', {
            'posts': posts, 'categories': categories, 'active_cat': category,
        })


class BlogDetailView(View):
    def get(self, request, slug):
        post     = get_object_or_404(BlogPost, slug=slug)
        related  = BlogPost.objects.filter(category=post.category).exclude(pk=post.pk)[:3]
        return render(request, 'pages/blog_detail.html', {'post': post, 'related': related})


class CareerView(View):
    def get(self, request):
        dept   = request.GET.get('dept', '')
        jtype  = request.GET.get('type', '')
        search = request.GET.get('q', '')
        jobs   = Job.objects.filter(is_active=True)
        if dept:
            jobs = jobs.filter(department=dept)
        if jtype:
            jobs = jobs.filter(job_type=jtype)
        if search:
            from django.db.models import Q
            jobs = jobs.filter(Q(title__icontains=search) | Q(company_name__icontains=search) | Q(location__icontains=search))
        departments = Job.objects.filter(is_active=True).values_list('department', flat=True).distinct()
        return render(request, 'pages/career.html', {
            'jobs':         jobs,
            'departments':  departments,
            'active_dept':  dept,
            'active_type':  jtype,
            'search':       search,
            'career_stats': [('6', 'Open Positions'), ('48', 'States Covered'), ('24/7', 'Dispatch Operations')],
            'perks':        CareerPerk.objects.all(),
        })


class ApplyView(View):
    def post(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id, is_active=True)
        except Job.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Job not found'}, status=404)

        name  = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        if not name or not email:
            return JsonResponse({'ok': False, 'error': 'Name and email are required'}, status=400)

        JobApplication.objects.create(
            job        = job,
            name       = name,
            email      = email,
            phone      = request.POST.get('phone', '').strip(),
            cover_note = request.POST.get('cover_note', '').strip(),
            cv_file    = request.FILES.get('cv_file'),
        )
        return JsonResponse({'ok': True})


class FAQView(View):
    def get(self, request):
        return render(request, 'pages/faq.html', {
            'faq_items': FaqItem.objects.all(),
        })


class SupportView(View):
    def _ctx(self, form, success=False):
        return {
            'form':             form,
            'success':          success,
            'support_channels': SupportChannel.objects.all(),
            'faq_items':        FaqItem.objects.all()[:5],
        }

    def get(self, request):
        return render(request, 'pages/support.html', self._ctx(ContactForm()))

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            Contact.objects.create(
                name=d['name'], email=d['email'], phone=d.get('phone', ''),
                subject=d['subject'], message=d['message'],
            )
            return render(request, 'pages/support.html', self._ctx(ContactForm(), success=True))
        return render(request, 'pages/support.html', self._ctx(form))


class CostCalculatorView(View):
    """Backend-only cost calculation — formula never exposed to frontend."""

    DOMESTIC = {'west-coast-usa', 'east-coast-usa', 'south-usa',
                'midwest-usa', 'mountain-usa', 'canada', 'mexico'}

    def post(self, request):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, Exception):
            return JsonResponse({'error': 'Invalid request'}, status=400)

        origin_label = (data.get('origin') or '').strip()
        dest_label   = (data.get('destination') or '').strip()
        truck_key    = (data.get('truck_key') or '').strip()
        cargo_key    = (data.get('cargo_key') or '').strip()

        if not all([origin_label, dest_label, truck_key, cargo_key]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # ── Look up cities ────────────────────────────────────────────────────
        def parse_city(label):
            i = label.rfind(', ')
            if i > 0:
                return label[:i], label[i+2:]
            return label, ''

        o_name, o_country = parse_city(origin_label)
        d_name, d_country = parse_city(dest_label)

        orig = PortCity.objects.filter(name=o_name, country=o_country, is_active=True).first()
        dest = PortCity.objects.filter(name=d_name, country=d_country, is_active=True).first()

        if not orig or not dest:
            return JsonResponse({'error': 'City not found — please select from the list'}, status=400)
        if orig.lat is None or dest.lat is None:
            return JsonResponse({'error': 'Coordinates not available for selected city'}, status=400)

        # ── Look up truck and cargo types ─────────────────────────────────────
        truck = TruckType.objects.filter(key=truck_key, is_active=True).first()
        cargo = CargoType.objects.filter(key=cargo_key, is_active=True).first()

        if not truck or not cargo:
            return JsonResponse({'error': 'Invalid vessel size or cargo type'}, status=400)

        # ── Get road distance via OSRM ────────────────────────────────────────
        is_domestic = (
            orig.zone and dest.zone and
            orig.zone.key in self.DOMESTIC and
            dest.zone.key in self.DOMESTIC
        )

        route_coords = None
        miles = None
        duration = None

        if is_domestic:
            osrm = _osrm_route(orig.lat, orig.lng, dest.lat, dest.lng)
            if osrm:
                miles        = osrm['miles']
                duration     = osrm['duration']
                route_coords = osrm['coords']

        if not miles:
            factor = 1.22 if is_domestic else 1.35
            miles  = round(_haversine(orig.lat, orig.lng, dest.lat, dest.lng) * factor)

        # ── Cost formula (100% backend-controlled) ────────────────────────────
        rate_per_mile   = float(truck.rate_per_mile)
        min_charge      = float(truck.min_charge)
        fuel_pct        = float(truck.fuel_surcharge_pct)
        cargo_mult      = float(cargo.multiplier)

        base_rate       = max(min_charge, rate_per_mile * miles)
        fuel_amount     = base_rate * (fuel_pct / 100)
        cargo_amount    = base_rate * (cargo_mult - 1)
        total           = base_rate + fuel_amount + cargo_amount
        total_low       = round(total * 0.90 / 10) * 10
        total_high      = round(total * 1.10 / 10) * 10
        transit_days    = max(1, round(miles / 500))
        transit_str     = '1' if transit_days == 1 else f'{transit_days}–{transit_days + 1}'

        return JsonResponse({
            'success':        True,
            'miles':          miles,
            'duration':       duration or f'{transit_str} days',
            'transit':        transit_str,
            'base_rate':      round(base_rate),
            'fuel_surcharge': round(fuel_amount),
            'cargo_adj':      round(cargo_amount),
            'total_low':      total_low,
            'total_high':     total_high,
            'cost_per_mile':  round(total / miles, 2) if miles else 0,
            'rate_label':     f'${rate_per_mile}/mi × {miles:,} mi',
            'fuel_label':     f'Fuel Surcharge ({fuel_pct:.0f}%)',
            'truck_name':     truck.name,
            'cargo_name':     cargo.name,
            'route_coords':   route_coords,
            'origin':         {'lat': orig.lat, 'lng': orig.lng, 'label': origin_label},
            'dest':           {'lat': dest.lat, 'lng': dest.lng, 'label': dest_label},
        })


@method_decorator(staff_member_required(login_url='/admin/login/'), name='dispatch')
class AdminGuideView(View):
    def get(self, request):
        return render(request, 'admin-guide.html')
