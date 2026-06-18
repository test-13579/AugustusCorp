from django import forms

SERVICE_CHOICES = [
    ('', '— Select a service —'),
    ('OTR (Over-the-Road Trucking)', 'OTR (Over-the-Road Trucking)'),
    ('Drayage (Port & Rail)', 'Drayage (Port & Rail)'),
    ('Intermodal Transportation', 'Intermodal Transportation'),
    ('Full Truckload (FTL)', 'Full Truckload (FTL)'),
    ('Less Than Truckload (LTL)', 'Less Than Truckload (LTL)'),
    ('Reefer (Temperature-Controlled)', 'Reefer (Temperature-Controlled)'),
    ('Heavy & Oversized Loads', 'Heavy & Oversized Loads'),
    ('Hazmat', 'Hazmat'),
    ('Cross-Border (USA–Canada)', 'Cross-Border (USA–Canada)'),
    ('Multi-Service / Other', 'Multi-Service / Other'),
]

FIELD_ATTRS = {'class': 'w-full border border-blue-200 rounded-sm px-4 py-3 text-gray-700 bg-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors text-sm'}
SELECT_ATTRS = {'class': 'w-full border border-blue-200 rounded-sm px-4 py-3 text-gray-700 bg-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm'}
TEXTAREA_ATTRS = dict(FIELD_ATTRS, rows=5, style='resize:none')


class TrackingForm(forms.Form):
    tracking_number = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'Enter tracking number (e.g. SWAY-2025-001)', 'class': FIELD_ATTRS['class'] + ' pl-11'}),
    )


class QuoteForm(forms.Form):
    name         = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your full name'}))
    email        = forms.EmailField(               widget=forms.EmailInput(attrs={**FIELD_ATTRS, 'placeholder': 'your@company.com'}))
    phone        = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': '+1 (800) 000-0000'}))
    company      = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'Company Ltd.'}))
    service_type = forms.ChoiceField(choices=SERVICE_CHOICES, widget=forms.Select(attrs=SELECT_ATTRS))
    origin       = forms.CharField(max_length=100, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'e.g. Los Angeles, CA'}))
    destination  = forms.CharField(max_length=100, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'e.g. Chicago, IL'}))
    weight       = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'e.g. 20,000 lbs / 10 pallets'}))
    dimensions   = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'e.g. 48" × 40" pallets, 53ft trailer'}))
    message      = forms.CharField(required=False, widget=forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Hazmat class, temperature requirements, special instructions, pickup date…'}))


class ContactForm(forms.Form):
    name    = forms.CharField(max_length=100,  widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'Your name'}))
    email   = forms.EmailField(               widget=forms.EmailInput(attrs={**FIELD_ATTRS, 'placeholder': 'your@email.com'}))
    phone   = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': '+1 (800) 000-0000'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={**FIELD_ATTRS, 'placeholder': 'How can we help?'}))
    message = forms.CharField(min_length=10,  widget=forms.Textarea(attrs={**TEXTAREA_ATTRS, 'placeholder': 'Tell us about your cargo requirements…'}))
