from django.contrib import admin
from .models import Catalog, CatalogCategory, Product, ProductDetail, \
    ProductAttribute, ProductColor, ProductSize, ProductImage,\
    ProductBrand


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    max_num = 10


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra =0
    max_num = 5


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'description', 'pub_date')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Catalog, CatalogAdmin)


class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'parent')


admin.site.register(CatalogCategory, CatalogCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'active','description', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        ProductImageInline,
        ProductSizeInline,
        ProductColorInline,
    ]


admin.site.register(Product, ProductAdmin)


class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')


admin.site.register(ProductDetail, ProductDetailAdmin)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(ProductAttribute, ProductAttributeAdmin)


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['product', 'color']

admin.site.register(ProductColor, ProductColorAdmin)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size']

admin.site.register(ProductSize, ProductSizeAdmin)


class ProductBrandAdmin(admin.ModelAdmin):
    list_display = [ 'brand']

admin.site.register(ProductBrand, ProductBrandAdmin)


