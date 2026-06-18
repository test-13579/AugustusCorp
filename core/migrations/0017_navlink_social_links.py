from django.db import migrations, models

INITIAL_NAV_LINKS = [
    ('Home',         '/'),
    ('About Us',     '/about/'),
    ('Our Services', '/services/'),
    ('Our Partners', '/companies/'),
    ('Career',       '/career/'),
    ('News',         '/blog/'),
    ('FAQ',          '/faq/'),
    ('Contact',      '/contact/'),
    ('Support',      '/support/'),
]


def seed_nav_links(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    for i, (label, url) in enumerate(INITIAL_NAV_LINKS):
        NavLink.objects.create(label=label, url=url, order=i, is_active=True)


def unseed_nav_links(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    NavLink.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_add_job_application'),
    ]

    operations = [
        # Social media fields on SiteSettings
        migrations.AddField(
            model_name='sitesettings',
            name='social_facebook',
            field=models.URLField(blank=True, default='', help_text='Facebook page URL (leave blank to hide icon)', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='social_linkedin',
            field=models.URLField(blank=True, default='', help_text='LinkedIn company/profile URL (leave blank to hide icon)', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='social_twitter',
            field=models.URLField(blank=True, default='', help_text='Twitter / X profile URL (leave blank to hide icon)', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='social_reddit',
            field=models.URLField(blank=True, default='', help_text='Reddit community URL (leave blank to hide icon)', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='social_instagram',
            field=models.URLField(blank=True, default='', help_text='Instagram profile URL (leave blank to hide icon)', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='social_youtube',
            field=models.URLField(blank=True, default='', help_text='YouTube channel URL (leave blank to hide icon)', max_length=200),
        ),
        # NavLink table
        migrations.CreateModel(
            name='NavLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Text shown in the navigation bar', max_length=60)),
                ('url', models.CharField(help_text='Absolute path or full URL, e.g. /about/ or https://…', max_length=200)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower number = appears first')),
                ('is_active', models.BooleanField(default=True, help_text='Uncheck to hide from nav without deleting')),
            ],
            options={
                'verbose_name': 'Nav Link',
                'verbose_name_plural': 'Nav Links',
                'ordering': ['order'],
            },
        ),
        # Seed initial rows so the nav works out of the box
        migrations.RunPython(seed_nav_links, unseed_nav_links),
    ]
