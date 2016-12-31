from django.conf.urls import url
from .views import CartDetail, CartAdd, CartRemove


urlpatterns = [
    url(r'^$', CartDetail.as_view(), name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', CartAdd.as_view(), name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$', CartRemove.as_view(), name='cart_remove'),
]
