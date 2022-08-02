from django.contrib import admin
from . models import Customer

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'fullname',
        'username',
        'email',
        'profile_pix',
        'social_handle'
    )


admin.site.register(Customer, CustomerAdmin)
