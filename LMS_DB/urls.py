from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    url(r'admin/',admin.site.urls),
    url(r'admin-panel/',views.admin_panel,name='admin-panel'),
    url(r'logout/', views.logout, name ='logout'),
    url(r'^$',views.index, name='index1'),
    url(r'events/',views.events_list, name ='events'),
    url(r'^(?P<event_id>[0-9]+)/$',views.event_details, name='details'),
    url(r'^(?P<event_id>[0-9]+)/edit$',views.Edit_event.as_view(), name='edit'),
    url(r'^(?P<event_id>[0-9]+)/view_layout$', views.view_layout, name='view_layout'),
    # url(r'^(?P<event_id>[0-9]+)/confirmation$',views.book_tickets, name='book'),
    url(r'^(?P<event_id>[0-9]+)/reserve$',views.reserve, name='reserve'),
    url(r'^(?P<event_id>[0-9]+)/reserve/payment$',views.payment, name='payment'),
    url(r'event/add$', views.Add_Event.as_view(), name = 'add'),
    url(r'^(?P<user>[0-9]+)/user-dashboard/', views.dashboard, name= 'dashboard'),
    url(r'^(?P<user>[0-9]+)/user-dashboard-settings/', views.dashboard_settings, name= 'dashboard-settings'),
    url(r'^(?P<user>[0-9]+)/user-dashboard-purchase-history/', views.dashboard_history, name='dashboard-history'),
    url(r'^(?P<user>[0-9]+)/user-event/', views.dashboard_event, name='dashboard_event'),
    url(r'^(?P<event_id>[0-9]+)/reserve/payment/handlerequest/', views.handlerequest, name='handlerequest'),
    url(r'signup/', views.sign_up, name='sign_up'),
]