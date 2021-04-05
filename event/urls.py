"""event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from . import views
#static file import
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

urlpatterns = [
    url(r'^LMS_DB/', include('LMS_DB.urls')),
    path('',views.home, name='home'),
    path('admin/', admin.site.urls),
    # path('index1/',views.index1, name='index1'),
    path('about_us',views.about, name='about_us'),
    path('artists',views.artists, name='artists'),
    path('map',views.map, name='map'),
    path('login',views.login, name='login'),
    path('signup',views.signup, name='signup'),
    path('select',views.select, name='select'),
    path('events',views.events, name='events1'),
    path('contact',views.contact, name='contact'),
    path('contact',views.details, name='details1'),
    path('add_events', views.event_add, name = 'event_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
