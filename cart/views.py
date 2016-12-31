from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, ProductBrand, CatalogCategory
from .cart import Cart
from .forms import CartAddProductForm
from django.views import View
from analytics.models import ClickEvent
import random


class CartAdd(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        ClickEvent.objects.create_event(product)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     product_size=cd['product_size'],
                     product_color=cd['product_color'],
                     update_quantity=cd['update'],
                     )
            #print(form)
        return redirect('cart:cart_detail')


class CartRemove(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetail(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                       'update': True})

        context = {
            'cart': cart,
            'categories': CatalogCategory.objects.all(),
            'randomone': sorted(Product.objects.all(), key=lambda x: random.random())[0],
            'randomtwo': sorted(Product.objects.all(), key=lambda x: random.random())[0],
            'best_seler': Product.objects.filter(best_seller=True)[:3],
            'brands': ProductBrand.objects.all(),
            'title': 'SHOPPING CART'
        }
        return render(request, 'cart/detail.html', context)

