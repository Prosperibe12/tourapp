from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from . forms import CheckoutForm
from .models import Tour, Cart, CartProduct, Banner, Order

# Create your views here.
def  index(request):
    # banner
    banner = Banner.objects.all()
    # content
    main = Tour.objects.all().order_by('-created')
    # paginator
    paginator = Paginator(main, 3)
    page_number = request.GET.get('page')
    place_list = paginator.get_page(page_number)
    
    # items in cart
    try:
        items = CartProduct.objects.filter(user = request.user.customer)
        items_count = items.count()
    except:
        items = CartProduct.objects.all()
        items_count = items.count()
            
    context= {
        'banner': banner,
        'Title': 'Home Page',
        'shows': main,
        'paginator': place_list,
        'count': items_count
    }
    return render(request, 'tour/index.html', context)


def overview(request, id):
    
    # get details of tour on id request
    mains = Tour.objects.get(id=id)
    day = mains.get_day
    
    context = {
        'main': mains,
        'Title': 'Tour Details',
        'day': day
    }
    return render(request, 'tour/overview.html', context)


# search function
def search(request):
  
    if request.method == 'GET':
        kword = request.GET.get('q')
        main = Tour.objects.filter(Q(name__icontains = kword) | Q(destination__icontains = kword))
    
    context = {
        'result': main,
        'Title': 'Search Page'
    }
    return render(request, 'tour/search.html', context)
    
    
def addtocart(request, id):
    
    # get Tour place by id
    cart_product = Tour.objects.get(id=id)
    print(cart_product)
    # check if cart exist in session
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)
        this_product_in_cart = cart_item.cartproduct_set.filter(place=cart_product)
        
        # assign cart to user
        if request.user.is_authenticated and request.user.customer:
            cart_item.customer = request.user.customer 
            cart_item.save()
            
        # checking if item exist in cart
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.per_person += 1
            cartproduct.subtotal += cart_product.price 
            cart_product.save()
            cart_item.total = cart_product.price 
            cart_item.save()
            messages.success(request, 'Item has been Increased.')           
        # add item in cart
        else:
            cartproduct = CartProduct.objects.create(cart=cart_item, place=cart_product, rate=cart_product.price, per_person=1, subtotal=cart_product.price)
            cart_item.total += cart_product.price 
            cart_item.save()
            messages.success(request, 'New Item Added in Cart')         
    else:
        cart_item = Cart.objects.create(total=0)
        print(f'Hello:::{cart_item.id}')  
        # how is line 89 saving without cart_item.save()
        request.session['cart_id'] = cart_item.id 
        print(f'hello:::{request.session["cart_id"]}')
        # same question above applies
        cartproduct = CartProduct.objects.create(cart=cart_item, place=cart_product, rate=cart_product.price, per_person=1, subtotal=cart_product.price)
        cart_item.total += cart_product.price 
        cart_item.save()
        messages.success(request, 'New Item Added')
        
    return redirect('index')

# users cart
def myCart(request):
    
    # get session cart
    cart_id = request.session.get('cart_id', None)
    # if cart_id exist
    if cart_id:
        cart_item = Cart.objects.get(id=cart_id)
        # if user is authenticated or customer
        if request.user.is_authenticated and request.user.customer:
            cart_item.customer = request.user.customer 
            cart_item.save()
    else:
        cart_item = None 
        
    context = {
        'Title':'Cart Page',
        'cart': cart_item
    }
    return render(request, 'tour/mycart.html', context)

# function to manage cart
def manageCart(request, id):
    
    # get action via url
    action = request.GET.get('action')
    # get id
    cart_obj = CartProduct.objects.get(id=id)
    # access cart
    cart = cart_obj.cart
    
    if action == 'increase':
        cart_obj.per_person += 1
        cart_obj.subtotal += cart_obj.rate 
        cart_obj.save()
        cart.total += cart_obj.rate 
        cart.save()
        messages.success(request, 'Item Increased')
    elif action == 'decrease':
        cart_obj.per_person -= 1
        cart_obj.subtotal -= cart_obj.rate 
        cart_obj.save()
        cart.total -= cart_obj.rate 
        cart.save()
        messages.success(request, 'Item Decreased')
        
        # check if nothing is in cart
        if cart_obj.per_person == 0:
            cart_obj.delete()
            
    elif action == 'remove':
        cart.total -= cart_obj.subtotal
        cart.save()
        cart_obj.delete()
    else:
        pass
        
    return redirect('mycart')

# clear cart
def clearCart(request):
    
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart = Cart.objects.get(id = cart_id)
        if request.user.is_authenticated and request.user.customer:
            cart.customer = request.user.customer 
            cart.save()
            
        cart.cartproduct_set.all().delete()
        cart.total = 0
        cart.save()
        messages.success(request, 'Cart Item has been deleted')
        return redirect('mycart')
    
    
def checkout(request):
    
    card_id = request.session.get('cart_id', None)
    cart_obj = Cart.objects.get(id=card_id)
    
    form = CheckoutForm 
    
    # check authentication
    if request.user.is_authenticated and request.user.customer:
        pass 
    else:
        return redirect('/users/loginuser/?next=/checkout/')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.cart = cart_obj 
            form.amount = cart_obj.total 
            form.subtotal = cart_obj.total
            form.discount = 0 
            form.order_status = 'Payment Received'
            paymethod = form.payment_method 
            del request.session['cart_id']
            paymethod = form.payment_method 
            form.save()
            
            order = form.id 
            if paymethod == 'Paystack':
                return redirect('payment', id=order)
    
    context = {
        'form': form,
        'Title': 'Checkout Page',
        'cart': cart_obj
    }
    return render(request, 'tour/checkout.html', context)
    
# payment
def paymentPage(request, id):
    
    orders = Order.objects.get(id=id)
    context = {
        'order': orders,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'tour/payment.html', context)  

# verify payment
def verify_payment(request:HttpRequest, ref:str)->HttpResponse:
    
    payment = get_object_or_404(Order, ref=ref)
    # what task is performed when the verify_payment() is called as it relates to line 228
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Payment Successful')
    else:
        messages.error(request, 'Payment Failed')
    return redirect('dashboard')