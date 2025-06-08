"""
URL configuration for greencycle project.

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
from django.urls import path
from core.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.views import *

class LogoutViewAllowGET(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='homepage.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('order-veggies/', order_veggies, name='order_veggies'),
    path('profile/', profile, name='profile'),
    path('logout/', TemplateView.as_view(template_name='logout.html'), name='logout_page'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    path('checkout/', checkout, name='checkout'),
    path('logout-confirm/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('admin/', admin.site.urls),
    path('compost_exchange/', compost_exchange, name='compost_exchange'),
    path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files (CSS, JS)
urlpatterns += staticfiles_urlpatterns()