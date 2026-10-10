from django.contrib import admin

from .models import (
    AccessSession,
    Advertisement,
    AdvertisementMetric,
    AuditLog,
    Customer,
    InternetPlan,
    MikrotikRouter,
    PaymentRecord,
    Tenant,
    TenantMembership,
    TenantSettings,
)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'domain', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')


@admin.register(TenantMembership)
class TenantMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'role')
    list_filter = ('role',)


@admin.register(TenantSettings)
class TenantSettingsAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'wifi_name', 'portal_title')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'identifier', 'name', 'phone', 'is_blocked')
    search_fields = ('name', 'identifier', 'phone')
    list_filter = ('is_blocked', 'tenant')


@admin.register(InternetPlan)
class InternetPlanAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'name', 'duration_minutes', 'price', 'is_active')
    list_filter = ('is_active', 'tenant')


@admin.register(AccessSession)
class AccessSessionAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'customer', 'plan', 'status', 'started_at')
    list_filter = ('status', 'tenant')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'title', 'is_active', 'starts_at', 'ends_at')
    list_filter = ('is_active', 'tenant')


@admin.register(AdvertisementMetric)
class AdvertisementMetricAdmin(admin.ModelAdmin):
    list_display = ('advertisement', 'impressions', 'clicks')


@admin.register(MikrotikRouter)
class MikrotikRouterAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'name', 'ip_address', 'is_online', 'last_seen_at')
    list_filter = ('is_online', 'tenant')


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'customer', 'amount', 'provider', 'status')
    list_filter = ('status', 'provider', 'tenant')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'actor', 'created_at')
    search_fields = ('message', 'actor')
