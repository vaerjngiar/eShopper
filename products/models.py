from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse
from decimal import Decimal


# class ProductQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)


class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(ProductManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_sale_price(self, percent=None):
        qs = Product.objects.filter(id__gte=1)
        new_price = 0
        for q in qs:
            q.sale_price *= Decimal(1+percent/100)
            #print(q.id)
            q.save()
            new_price += 1
        return "New price made: {i}".format(i=new_price)

    def refresh_price(self, percent=None):
        qs = Product.objects.filter(id__gte=1)
        new_price = 0
        for q in qs:
            q.price *= Decimal(1+percent/100)
            #print(q.id)
            q.save()
            new_price += 1
        return "New sale_price made: {i}".format(i=new_price)


class Catalog(models.Model):
    '''
    The ``Catalog`` model represents a collection of products for
    sale. A catalog contains additional information like name,
    publisher, a short description, and a publication date.
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150)
    publisher = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class CatalogCategory(models.Model):
    '''
    The ``Category`` model represents a category within a specific
    ``Catalog`` object. Categories contain a ForeignKey to their
    catalog, as well as an optional ForeignKey to another category
    that will serve as a parent category.
    '''
    catalog = models.ForeignKey('Catalog', related_name='categories')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class ProductBrand(models.Model):
    '''
        The ``Product`` model represents a particular information about
        product brand
        '''
    brand = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('brand',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.brand

    def get_absolute_url(self):
        return reverse('shop:product_list_by_brand', args=[self.slug])


class Product(models.Model):
    '''
    The ``Product`` model represents a particular item in a catalog of
    products. It contains information about the product for sale,
    which is common to all items in the catalog. These include, for
    example, the item's price, manufacturer, an image or photo, a
    description, etc.
    '''
    category = models.ForeignKey('CatalogCategory', related_name='products')
    brand = models.ForeignKey('ProductBrand', related_name='brands')
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)
    description = models.TextField()
    photo1 = models.ImageField(upload_to='product_photo', blank=True)
    photo2 = models.ImageField(upload_to='product_photo', blank=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=12, blank=True)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    active = models.BooleanField(default=True)
    new = models.BooleanField(default=True)
    best_seller = models.BooleanField(default=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"pk": self.pk})


class ProductDetail(models.Model):
    '''
    The ``ProductDetail`` model represents information unique to a
    specific product. This is a generic design that can be used to
    extend the information contained in the ``Product`` model with
    specific, extra details.
    '''
    product = models.ForeignKey('Product', related_name='details')
    attribute = models.ForeignKey('ProductAttribute')
    value = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s: %s' % (self.product, self.attribute)


class ProductAttribute(models.Model):
    '''
    The ``ProductAttribute`` model represents a class of feature found
    across a set of products. It does not store any data values
    related to the attribute, but only describes what kind of a
    product feature we are trying to capture.

    Possible attributes include things like materials, colors, sizes,
    and many, many more.
    '''
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProductColor(models.Model):
    '''
    The ``Product`` model represents a particular information about
    product colors
    '''
    product = models.ForeignKey(Product, related_name='colors')
    color = models.CharField(max_length=50)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.color


class ProductSize(models.Model):
    '''
    The ``Product`` model represents a particular information about
    product sizes
    '''
    product = models.ForeignKey(Product, related_name='sizes')
    size = models.CharField(max_length=12)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.size


class ProductImage(models.Model):
    '''
    The ``Product`` model store additional products images
    '''
    product = models.ForeignKey(Product, related_name='images')
    image = models.ImageField(upload_to='product_photo', blank=True)

    def __str__(self):
        return self.product.name
