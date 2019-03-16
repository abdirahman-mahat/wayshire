from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .forms import *
from .views import *
from . import views
urlpatterns=[
url(r'^$', views.dashboard, name='dashboard'),
url(r'^home/$', views.index, name='home'),
url(r'^finance/$', views.finance, name='finance'),
url(r'^loading/$', views.loading, name='loading'),
url(r'^loading_dashboard/$', views.loading_dashboard, name='loading_dashboard'),
url(r'^delivery/edit/(?P<delivery_id>\d+)/$', views.edit_delivery, name='edit_delivery'),

url(r'^fleet/(?P<truck_id>\d+)/$', views.show, name='show'),
url(r'^order/$', views.order, name='order'),
url(r'^order/(?P<order_id>\d+)/$', views.show_order, name='show_order'),
url(r'^order/edit/(?P<order_id>\d+)/$', views.edit_order, name='edit_order'),
url(r'^loading/edit/(?P<order_id>\d+)/$', views.loading_status, name='edit_loading'),
url(r'^change_password/$', views.change_password, name='change_password'),
url(
        r'^truck-autocomplete/$',
        TruckAutoComplete.as_view(),
        name='truck-autocomplete',
    ),
url(r'^toadays_orders/$', views.orders_today, name='todays_orders'),
url(r'^delivery/$', views.delivery, name='delivery'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
