from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.storage import staticfiles_storage
from .models import SiteSettings
from . import views

def favicon(request):
    s = SiteSettings.get()
    if s.favicon:
        return HttpResponseRedirect(s.favicon.url)
    return HttpResponseRedirect(staticfiles_storage.url('images/logo.svg'))

urlpatterns = [
    path('favicon.ico', favicon),
    path('api/calculate-cost/', views.CostCalculatorView.as_view(), name='calculate_cost'),
    path('admin-guide/', views.AdminGuideView.as_view(), name='admin_guide'),
    path('',           views.HomeView.as_view(),      name='home'),
    path('about/',     views.AboutView.as_view(),     name='about'),
    path('services/',  views.ServicesView.as_view(),  name='services'),
    path('companies/', views.CompaniesView.as_view(), name='companies'),
    path('track/',     views.TrackView.as_view(),     name='track'),
    path('quote/',     views.QuoteView.as_view(),     name='quote'),
    path('contact/',   views.ContactView.as_view(),   name='contact'),
    path('blog/',           views.BlogView.as_view(),       name='blog'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('career/',    views.CareerView.as_view(),    name='career'),
    path('career/apply/<int:job_id>/', views.ApplyView.as_view(), name='apply'),
    path('faq/',       views.FAQView.as_view(),       name='faq'),
    path('support/',   views.SupportView.as_view(),   name='support'),
]
