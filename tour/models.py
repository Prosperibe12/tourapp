from datetime import datetime
from distutils.command.upload import upload
from email.mime.image import MIMEImage
import secrets
from django.db import models
from django.forms import CharField
from multiselectfield import MultiSelectField
from dateutil.relativedelta import relativedelta
from users.models import Customer
from .paystack import PayStack

# Create your models here.
class Banner(models.Model):
    
    image = models.ImageField(upload_to='banners')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f'{self.image}'
    
        
class Tour(models.Model):
    
    PACKAGES = (
        ('Air Fares', 'Air Fares'),
        ('4 Nights Hotel Accomodation', '4 Nights Hotel Accomodation'),
        ('Entrance Fee', 'Entrance Fee'),
        ('Tour Guide', 'Tour Guide'),
    )
    
    name = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    description = models.TextField()
    age_range = models.IntegerField()
    price = models.IntegerField()
    main_photo = models.ImageField(upload_to='photos')
    photo1 = models.ImageField(upload_to='photos')
    photo2 = models.ImageField(upload_to='photos')
    photo3 = models.ImageField(upload_to='photos')
    refund_policy = models.CharField(max_length=100)
    package = MultiSelectField(max_length=200, choices=PACKAGES, null=True, blank=True)
    departure = models.DateTimeField(default=datetime.now)
    arrival = models.DateTimeField(default=datetime.now)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}::: {self.destination}'
    
    @property
    def get_day(self):
        day = (self.arrival - self.departure).days
        return day


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'cart:::{str(self.id)}'
    
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    place = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    per_person = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'caer:::{str(self.cart.id)} - cartproduct ::: {str(self.id)}'
    

ORDER_STATUS = (
    ('Payment Received', 'Payment Received'),
    ('Payment Completed', 'Payment Completed'),
    ('Order Canceled', 'Order Canceled'),
)

METHOD = (
    ('Paystack', 'Paystack'),
)

class Order(models.Model):
    
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True, blank=True)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(null=True, blank=True)
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(null=True, blank=True)
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=200, choices=METHOD, default='Paystack')
    ref = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f'{self.order_status} ::: {str(self.id)}'
    
    # generate code
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(25)
            obj_with_sm_ref = Order.objects.filter(ref=ref)
            if not obj_with_sm_ref:
                self.ref = ref 
        super().save(*args, **kwargs)
        
    # function to make amount in kobo
    def amount_value(self)->int:
        return self.amount * 100 
    
    # verify payment
    def verify_payment(self):
        
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        
        if status:
            if result['amount']/100 == self.amount:
               self.payment_completed = True 
            self.save() 
               
        if self.order_status == 'Payment Completed':
            self.save()
            self.cart.delete()
        if self.payment_completed:
            return True 
        return False 
    