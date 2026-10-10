from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Customer, InternetPlan, Tenant, TenantMembership
from .views import get_tenant_queryset

User = get_user_model()


class NovaInfoCoreTests(TestCase):
    def setUp(self):
        self.tenant_a = Tenant.objects.create(name='Restaurante Aurora', slug='restaurante-aurora')
        self.tenant_b = Tenant.objects.create(name='Hotel Sol', slug='hotel-sol')

        self.user_a = User.objects.create_user(username='restaurante_admin', password='secret123')
        self.user_b = User.objects.create_user(username='hotel_admin', password='secret456')

        TenantMembership.objects.create(user=self.user_a, tenant=self.tenant_a, role='owner')
        TenantMembership.objects.create(user=self.user_b, tenant=self.tenant_b, role='owner')

        self.customer_a = Customer.objects.create(
            tenant=self.tenant_a,
            identifier='CLI-001',
            name='Maria Souza',
            phone='11999990000',
        )
        self.customer_b = Customer.objects.create(
            tenant=self.tenant_b,
            identifier='CLI-002',
            name='João Pereira',
            phone='11999990001',
        )
        InternetPlan.objects.create(
            tenant=self.tenant_a,
            name='Acesso básico',
            duration_minutes=60,
            price=15,
        )
        InternetPlan.objects.create(
            tenant=self.tenant_b,
            name='Plano diário',
            duration_minutes=1440,
            price=30,
        )

    def test_home_page_renders(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transforme seu Wi‑Fi')

    def test_dashboard_requires_login(self):
        response = self.client.get('/painel/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/painel/login/', response.url)

    def test_tenant_queryset_filters_by_membership(self):
        qs = get_tenant_queryset(Customer, self.user_a)
        self.assertIn(self.customer_a, qs)
        self.assertNotIn(self.customer_b, qs)
