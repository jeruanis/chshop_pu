"""shopme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
import store


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('orders/', include('orders.urls')),
    path('currencies/', include('currencies.urls')),
    path('chatapp/', include('chatapp.urls')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('seller/', views.seller_doc, name='seller_doc'),
    path('services/', views.services_doc, name='services_doc'),
    path('api_doc/', views.api_doc, name='api_doc'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #for media folder files access
#assign the error views
handler400 = store.views.error_400
handler404 = store.views.error_404
handler500 = store.views.error_500
