from django.conf.urls import url
from .views import ProductListView, ProductDetailView, CategoryList, BrandList


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='products'),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),
    #url(r'^apply/$', views.size_apply, name='apply'),
    url(r'^(?P<category_slug>[-\w]+)/$', CategoryList.as_view(), name='product_list_by_category'),
    url(r'^brand/(?P<brand_slug>[-\w]+)/$', BrandList.as_view(), name='product_list_by_brand'),

]