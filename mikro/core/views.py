from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy

from .models import AccessSession, Advertisement, Customer, InternetPlan, MikrotikRouter, Tenant, TenantMembership


def get_current_tenant(user):
    if user.is_superuser:
        return None
    membership = getattr(user, 'tenant_membership', None)
    if membership is not None:
        return membership.tenant
    return None


def get_tenant_queryset(model_class, user):
    if user.is_superuser:
        return model_class.objects.all()
    tenant = get_current_tenant(user)
    if tenant is None:
        return model_class.objects.none()
    return model_class.objects.filter(tenant=tenant)


def home(request):
    tenants = Tenant.objects.filter(is_active=True)[:3]
    return render(request, 'home.html', {'tenants': tenants})


@login_required(login_url='/painel/login/')
def dashboard(request):
    tenant = get_current_tenant(request.user)
    if tenant is None and not request.user.is_superuser:
        return render(request, 'dashboard.html', {'tenant': None, 'customers': [], 'plans': [], 'routers': [], 'advertisements': [], 'stats': {}})

    customers = get_tenant_queryset(Customer, request.user)
    plans = get_tenant_queryset(InternetPlan, request.user)
    routers = get_tenant_queryset(MikrotikRouter, request.user)
    advertisements = get_tenant_queryset(Advertisement, request.user)
    sessions = get_tenant_queryset(AccessSession, request.user)

    stats = {
        'customers_online': sessions.filter(status='active').count(),
        'customers_registered': customers.count(),
        'revenue_today': 0,
        'monthly_revenue': 0,
        'accesses_sold': sessions.count(),
        'data_consumption': sessions.aggregate(total=Sum('data_used_mb'))['total'] or 0,
        'avg_session_minutes': 0,
        'routers_online': routers.filter(is_online=True).count(),
        'advertisement_views': advertisements.aggregate(total=Count('id'))['total'] or 0,
    }
    return render(request, 'dashboard.html', {
        'tenant': tenant,
        'customers': customers.order_by('-created_at')[:5],
        'plans': plans.order_by('-price')[:5],
        'routers': routers.order_by('-is_online', '-last_seen_at')[:5],
        'advertisements': advertisements.order_by('-created_at')[:5],
        'sessions': sessions.order_by('-started_at')[:5],
        'stats': stats,
    })


@login_required(login_url='/painel/login/')
def clients(request):
    customers = get_tenant_queryset(Customer, request.user).order_by('-created_at')
    return render(request, 'clients.html', {'customers': customers})


@login_required(login_url='/painel/login/')
def internet_plans(request):
    plans = get_tenant_queryset(InternetPlan, request.user).order_by('-price')
    return render(request, 'plans.html', {'plans': plans})


@login_required(login_url='/painel/login/')
def advertising(request):
    ads = get_tenant_queryset(Advertisement, request.user).order_by('-created_at')
    return render(request, 'advertising.html', {'ads': ads})


@login_required(login_url='/painel/login/')
def mikrotik(request):
    routers = get_tenant_queryset(MikrotikRouter, request.user).order_by('-last_seen_at')
    return render(request, 'mikrotik.html', {'routers': routers})


class NovaInfoLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Acessar painel Nova Info'
        return context


class NovaInfoLogoutView(LogoutView):
    next_page = reverse_lazy('/')
