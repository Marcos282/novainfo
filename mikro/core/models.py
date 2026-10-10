from django.db import models
from django.contrib.auth.models import User


class Tenant(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=150, blank=True, default='')
    brand_color = models.CharField(max_length=20, default='#071B33')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TenantMembership(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Superadministrador'),
        ('owner', 'Administrador do estabelecimento'),
        ('operator', 'Operador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_membership')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='owner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.tenant.name})'


class TenantSettings(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
    wifi_name = models.CharField(max_length=120, default='Wi-Fi Nova Info')
    portal_title = models.CharField(max_length=120, default='Wi-Fi Inteligente')
    logo_url = models.URLField(blank=True, default='')
    background_image = models.URLField(blank=True, default='')
    primary_color = models.CharField(max_length=20, default='#0066FF')
    secondary_color = models.CharField(max_length=20, default='#00D4FF')

    def __str__(self):
        return f'{self.tenant.name} settings'


class Customer(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='customers')
    identifier = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} ({self.identifier})'


class InternetPlan(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=120)
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    description = models.TextField(blank=True, default='')
    data_limit_mb = models.PositiveIntegerField(default=0)
    speed_limit_mbps = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.tenant.name}'


class AccessSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('pending_payment', 'Pendente de pagamento'),
        ('expired', 'Expirada'),
        ('closed', 'Encerrada'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='sessions')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    plan = models.ForeignKey(InternetPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    authorization_token = models.CharField(max_length=100, blank=True, default='')
    data_used_mb = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.tenant.name} - {self.status}'


class Advertisement(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='advertisements')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, default='')
    link = models.URLField(blank=True, default='')
    image_url = models.URLField(blank=True, default='')
    video_url = models.URLField(blank=True, default='')
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AdvertisementMetric(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='metrics')
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.advertisement.title} metrics'


class MikrotikRouter(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='routers')
    name = models.CharField(max_length=120)
    ip_address = models.GenericIPAddressField()
    model = models.CharField(max_length=120, default='CCR1009-7G-1C-1S+')
    routeros_version = models.CharField(max_length=30, default='7.14')
    device_identifier = models.CharField(max_length=80, unique=True)
    is_online = models.BooleanField(default=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.ip_address})'


class PaymentRecord(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    plan = models.ForeignKey(InternetPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    provider = models.CharField(max_length=40, default='Mercado Pago')
    status = models.CharField(max_length=25, default='pending')
    external_reference = models.CharField(max_length=80, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.provider} - {self.amount}'


class AuditLog(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='audit_logs')
    actor = models.CharField(max_length=100, default='system')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.actor} - {self.created_at}'
