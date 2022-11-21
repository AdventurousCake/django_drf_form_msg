"""django1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.views.generic import TemplateView

from django.contrib.auth import views

from core.views import core_auth
from django1.settings import ADMIN_PATH


urlpatterns = [
    path('admin/', admin.site.urls, name='admin_page'),
    # path(ADMIN_PATH+'/', admin.site.urls, name='admin_page'),

    # path('polls/', include('polls.urls'), name='polls'),
    # path('', include('home_page.urls'), name='home'),
    # path('simplesite1/', include('simplesite1_bstrap.urls')),
    # path('blog/', include('blog.urls')),
    # path('people/', include('people.urls')),
    # path('orders/', include('myshop_orders.urls', namespace='orders')),
    # path('cart/', include('myshop_cart.urls', namespace='cart')),
    # path('shop/', include('myshop.urls', namespace='shop')),
    #
    # # C WORK
    # path('anketa/', include('Anketa.urls'), name='anketa'),
    path('auth_github/', include('social_django.urls', namespace='social')),
    path('page_github/', core_auth),

    path('msg1/', include('FORM_MSG.urls')),


    # robots
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name='robots'),

    # debug tools
    path('__debug__/', include('debug_toolbar.urls')),
]

# api root; PRIVATE URL API
API_PATH = 'api/v1/'
if settings.IS_SERVER:
    API_PATH = settings.API_PATH
urlpatterns.append(path(API_PATH, include('api.urls', namespace='api')))


# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    # custom login
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
]

# check for nginx static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL)  # media root
