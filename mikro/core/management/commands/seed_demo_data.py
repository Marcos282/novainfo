from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    AccessSession,
    Advertisement,
    Customer,
    InternetPlan,
    MikrotikRouter,
    Tenant,
    TenantMembership,
    TenantSettings,
)


class Command(BaseCommand):
    help = 'Populate the database with demo data for the Nova Info SaaS prototype.'

    def handle(self, *args, **options):
        tenant, _ = Tenant.objects.get_or_create(
            slug='restaurante-aurora',
            defaults={
                'name': 'Restaurante Aurora',
                'domain': 'restaurante.novainfo.com.br',
                'brand_color': '#071B33',
                'is_active': True,
            },
        )

        TenantSettings.objects.get_or_create(
            tenant=tenant,
            defaults={
                'wifi_name': 'Aurora Wi‑Fi',
                'portal_title': 'Wi‑Fi Inteligente',
                'primary_color': '#0066FF',
                'secondary_color': '#00D4FF',
            },
        )

        for customer_data in [
            ('CLI-001', 'Maria Souza', '11999990000'),
            ('CLI-002', 'João Pereira', '11999990001'),
            ('CLI-003', 'Ana Costa', '11999990002'),
        ]:
            Customer.objects.get_or_create(
                tenant=tenant,
                identifier=customer_data[0],
                defaults={'name': customer_data[1], 'phone': customer_data[2], 'last_seen_at': timezone.now()},
            )

        for plan_data in [
            ('Acesso rápido', 30, 15.00, 10),
            ('Acesso básico', 60, 25.00, 20),
            ('Acesso diário', 1440, 95.00, 100),
        ]:
            InternetPlan.objects.get_or_create(
                tenant=tenant,
                name=plan_data[0],
                defaults={
                    'duration_minutes': plan_data[1],
                    'price': plan_data[2],
                    'speed_limit_mbps': plan_data[3],
                    'data_limit_mb': 2000,
                    'is_active': True,
                },
            )

        AccessSession.objects.get_or_create(
            tenant=tenant,
            authorization_token='auth-demo',
            defaults={'status': 'active', 'data_used_mb': 128},
        )

        Advertisement.objects.get_or_create(
            tenant=tenant,
            title='Promoção de pizza',
            defaults={
                'description': 'Peça duas pizzas grandes e ganhe um refrigerante.',
                'link': 'https://example.com/promocao',
                'is_active': True,
            },
        )

        MikrotikRouter.objects.get_or_create(
            tenant=tenant,
            device_identifier='router-demo-001',
            defaults={
                'name': 'MikroTik Core',
                'ip_address': '10.0.0.10',
                'model': 'CCR1009-7G-1C-1S+',
                'routeros_version': '7.14',
                'is_online': True,
                'last_seen_at': timezone.now(),
            },
        )

        if not TenantMembership.objects.filter(tenant=tenant).exists():
            User = get_user_model()
            user, _ = User.objects.get_or_create(username='tenant-admin-demo')
            user.set_password('novainfo123')
            user.save()
            TenantMembership.objects.create(user=user, tenant=tenant, role='owner')

        self.stdout.write(self.style.SUCCESS('Demo data populated for Restaurante Aurora'))
