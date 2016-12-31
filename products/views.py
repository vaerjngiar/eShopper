from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404, HttpResponseRedirect
from .models import Product, ProductDetail, ProductAttribute, CatalogCategory, Catalog, ProductBrand

from cart.forms import CartAddProductForm
from django.shortcuts import render, redirect

from analytics.models import ClickEvent
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View

#
# @require_POST
# def size_apply(request):
#     form = ProductSizeApplyForm(request.POST)
#     if form.is_valid():
#         size = form.cleaned_data['size']
#         try:
#             size = ProductSize.objects.get(size__iexact=size, in_stock=True)
#             request.session['size_id'] = size.id
#         except ProductSize.DoesNotExist:
#             request.session['size_id'] = None
#     return redirect('cart:cart_detail')


import random


class ProductListView(ListView):
    model = Product
    object_list = Product.objects.all()
    template_name = 'products/product_list.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        object_list = Product.objects.all()
        paginator = Paginator(object_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages)

        context['object_list'] = object_list
        context["title"] = 'e-Shoper Products'
        context['randomone'] = sorted(Product.objects.all(), key=lambda x: random.random())[0]
        context['randomtwo'] = sorted(Product.objects.all(), key=lambda x: random.random())[0]
        context['best_seler'] = Product.objects.filter(best_seller=True)[:3]
        context['categories'] = CatalogCategory.objects.all()
        context['brands'] = ProductBrand.objects.all()
        context['pages'] = paginator.page_range

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        instance = self.get_object()

        context["cart_product_form"] = CartAddProductForm
        context["title"] = instance.name
        context['randomone'] = sorted(Product.objects.all(), key=lambda x: random.random())[1]
        context['randomtwo'] = sorted(Product.objects.all(), key=lambda x: random.random())[1]
        context['best_seler'] = Product.objects.filter(best_seller=True)[:3]
        context['categories'] = CatalogCategory.objects.all()
        context['brands'] = ProductBrand.objects.all()

        return context

    # def get(self, request, pk=None, *args, **kwargs):
    #     # template_name = 'products/product_detail.html'
    #     qs = Product.objects.filter(pk__iexact=pk)
    #     if qs.count() != 1 and not qs.exists():
    #         raise Http404
    #     obj = qs.first()
    #     print(ClickEvent.objects.create_event(obj))
    #     return HttpResponseRedirect(obj.get_absolute_url)


class CategoryList(View):
    def get(self, request, category_slug=None,*args, **kwargs):
        category = None
        categories = CatalogCategory.objects.all()
        object_list = Product.objects.filter(active=True)
        if category_slug:
            category = get_object_or_404(CatalogCategory, slug=category_slug)
            object_list = object_list.filter(category=category)
        context = {'category': category,
                   'categories': categories,
                   'object_list': object_list,
                   'randomone': sorted(Product.objects.all(), key=lambda x: random.random())[2],
                   'randomtwo': sorted(Product.objects.all(), key=lambda x: random.random())[2],
                   'best_seler': Product.objects.filter(best_seller=True)[:3],
                   'brands': ProductBrand.objects.all()
                   }
        return render(request, 'products/product_list.html', context)


class BrandList(View):
    def get(self, request, brand_slug=None, *args, **kwargs):
        brand = None
        brands = ProductBrand.objects.all()
        object_list = Product.objects.filter(active=True)
        if brand_slug:
            brand = get_object_or_404(ProductBrand, slug=brand_slug)
            object_list = object_list.filter(brand=brand)
        context = {'brand': brand,
                   'brands': brands,
                   'object_list': object_list,
                   'randomone': sorted(Product.objects.all(), key=lambda x: random.random())[3],
                   'randomtwo': sorted(Product.objects.all(), key=lambda x: random.random())[3],
                   'best_seler': Product.objects.filter(best_seller=True)[:3],
                   'categories': CatalogCategory.objects.all(),
                   }
        return render(request, 'products/product_list.html', context)

