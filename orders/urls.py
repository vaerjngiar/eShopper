from django.conf.urls import url
from . import views
from orders.views import OrderCreate


urlpatterns = [
    url(r'^create/$', OrderCreate.as_view(), name='order_create'),
    url(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='admin_order_detail'),
]