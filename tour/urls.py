from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('overview/<str:id>/', views.overview, name='overview'),
    path('search/', views.search, name='search'),
    path('addtocart/<str:id>/', views.addtocart, name='addtocart'),
    path('mycart/', views.myCart, name='mycart'),
    path('manageCart/<str:id>/', views.manageCart, name='manageCart'),
    path('clearCart/', views.clearCart, name='clearCart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<str:id>/', views.paymentPage, name='payment'),
    path('<str:ref>/', views.verify_payment, name='verify-payment')
]