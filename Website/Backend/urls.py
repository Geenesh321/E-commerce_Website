from django.urls import path
from .views import *

app_name = 'Backend'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact-us/', ContactView.as_view(), name='contact'),
    path('allproducts/', AllProductView.as_view(), name='allproducts'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='productdetail'),
    path('add-to-cart/<int:pk>/', AddToCartView.as_view(), name='addtocart'),
    path('decrease-from-cart/<int:pk>/', DecreaseFromCartView.as_view(), name='decreasefromcart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchView.as_view(), name='search'),
]
