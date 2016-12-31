from decimal import Decimal
from django.conf import settings
from products.models import Product, ProductSize


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store curent productsize
        self.size_id = self.session.get('size_id')

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['sale_price'] = Decimal(item['sale_price'])
            item['total_price'] = item['sale_price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, product_size='-', product_color='-', update_quantity=False ):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'sale_price': str(product.sale_price),
                                     'product_size': '-',
                                     'product_color': '-',
                                     }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['product_size'] = product_size
            self.cart[product_id]['product_color'] = product_color


        else:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['product_size'] = product_size
            self.cart[product_id]['product_color'] = product_color
        print(product_size)
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def size(self):
        if self.size_id:
            return ProductSize.objects.get(id=self.size_id)
        return None

    def get_total_price(self):
        return sum(Decimal(item['sale_price']) * item['quantity'] for item in self.cart.values())
