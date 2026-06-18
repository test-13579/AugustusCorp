from .models import Service, SiteSettings, FaqItem, Office, WhyUsFeature, Job, NavLink

_FALLBACK_NAV = [
    ('Home',         '/'),
    ('About Us',     '/about/'),
    ('Our Services', '/services/'),
    ('Our Companies', '/companies/'),
    ('Career',       '/career/'),
    ('News',         '/blog/'),
    ('FAQ',          '/faq/'),
    ('Contact',      '/contact/'),
    ('Support',      '/support/'),
]


def global_context(request):
    nav_qs = list(NavLink.objects.filter(is_active=True).values_list('label', 'url'))
    return {
        'tab_links': nav_qs or _FALLBACK_NAV,
        'footer_services': Service.objects.all()[:6],
        'site': SiteSettings.get(),
        # chatbot data — exposed to every template via the partial
        'cb_services':   Service.objects.all(),
        'cb_faqs':       FaqItem.objects.all(),
        'cb_offices':    Office.objects.all(),
        'cb_why_us':     WhyUsFeature.objects.all(),
        'cb_jobs_count': Job.objects.filter(is_active=True).count(),
    }
