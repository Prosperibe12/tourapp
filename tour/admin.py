from django.contrib import admin
from . models import *

# Register your models here.
class TourAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'destination',
        'description',
        'age_range',
        'price',
        'main_photo',
        'photo1',
        'photo2',
        'photo3',
        'refund_policy',
        'package',
        'departure',
        'arrival',
        'created'
    )
    
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'total',
        'created_at'
    )
    
class CartProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'cart',
        'place',
        'rate',
        'per_person',
        'subtotal',
        'created_at'
    )
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'created_at')


admin.site.register(Tour, TourAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order)
admin.site.register(CartProduct, CartProductAdmin)
