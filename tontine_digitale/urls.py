"""
URL configuration for tontine_digitale project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from core.dashboard import dashboard_view
from core.auth_views import login_view, admin_dashboard_view
from core.commercant_views import (
    commercant_dashboard,
    commercant_participer,
    commercant_historique,
    commercant_profil
)

def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('login/', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('admin-panel/', admin_dashboard_view, name='admin_panel'),
    path('api/', include('core.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Routes commerçants
    path('commercant/dashboard/', commercant_dashboard, name='commercant_dashboard'),
    path('commercant/participer/', commercant_participer, name='commercant_participer'),
    path('commercant/historique/', commercant_historique, name='commercant_historique'),
    path('commercant/profil/', commercant_profil, name='commercant_profil'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
