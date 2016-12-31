from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from .models import Order, OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


class OrderCreate(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         sale_price=item['sale_price'],
                                         product_size=item['product_size'],
                                         product_color=item['product_color'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)

            context = {'order': order}
            return render(request, 'orders/order/creaded.html', context)

    def get(self, request, *args, ** kwargs):
        cart = Cart(request)
        form = OrderCreateForm()
        context = {'cart': cart,
                   'form': form,
                   'title': 'CHECK OUT',
                   }
        return render(request, 'orders/order/create.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


