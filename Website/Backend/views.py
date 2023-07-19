from .models import BasicDetails
from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **Kwargs):
        context = super().get_context_data(**Kwargs)
        product = Product.objects.all()
        context['products'] = product
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class AllProductView(TemplateView):
    template_name = 'allproduct.html'

    def get_context_data(self, **Kwargs):
        context = super().get_context_data(**Kwargs)
        category = Category.objects.all()
        context['categories'] = category
        return context


class ProductDetailView(TemplateView):
    template_name = 'ProductDetail.html'

    def get_context_data(self, **Kwargs):
        context = super().get_context_data(**Kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        context['product'] = product
        return context


class AddToCartView(View):
    template_name = 'addtocart.html'

    def get(self, request, pk):
        product_obj = get_object_or_404(Product, pk=pk)

        # Check if cart exists
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create(total=0)
            request.session['cart_id'] = cart.id

        # Check if the product is already in the cart
        cart_product = CartProduct.objects.filter(
            cart=cart, product=product_obj).first()
        if cart_product:
            cart_product.quantity += 1
        else:
            cart_product = CartProduct.objects.create(
                cart=cart,
                product=product_obj,
                rate=product_obj.selling_price,
                quantity=1,
                sub_total=product_obj.selling_price
            )

        cart_product.sub_total = cart_product.rate * cart_product.quantity
        cart_product.save()

        # Recalculate the total within the view
        cart.total += cart_product.sub_total
        cart.save()

        cart_items = CartProduct.objects.filter(cart=cart)
        context = {
            'cart_items': cart_items,
        }
        return render(request, self.template_name, context)


class DecreaseFromCartView(TemplateView):
    template_name = 'decreasefromcart.html'

    def get_context_data(self, **Kwargs):
        context = super().get_context_data(**Kwargs)
        product_id = self.kwargs['pk']
        print(product_id)
        product_obj = Product.objects.get(id=product_id)
        # check if cart exists
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            current_cart = Cart.objects.get(id=cart_id)
            cart_product = CartProduct.objects.filter(
                Q(cart=current_cart) & Q(product=product_obj)).first()
            if (cart_product):
                cart_product.quantity -= 2
                cart_product.sub_total -= product_obj.selling_price
                cart_product.save()
            else:
                cart_product.quantity = 0
                cart_product.save()

            setTotal(cart_id)
            context['total_price'] = current_cart.total

        context['product_id'] = product_id
        return context


def setTotal(cart_id):
    cart_obj = Cart.objects.get(id=cart_id)
    product_prices = CartProduct.objects.filter(
        cart=cart_obj).values_list('sub_total', flat=True)
    total_price = sum(product_prices)
    cart_obj.total = total_price
    cart_obj.save()


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Perform form validation
        if not full_name or not username or not email or not password:
            messages.error(request, 'Please fill in all the required fields.')
            return redirect('Backend:register')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('Backend:register')

        # Create a new user object
        user = User.objects.create_user(
            username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        # Create a Customer object linked to the user
        customer = Customer.objects.create(
            user=user, full_name=full_name, email=email)

        # Display success message
        messages.success(request, 'Registration successful.')
        return redirect('login')


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(reverse('Backend:home'))
        else:
            return render(request, self.template_name, {'error_message': 'Invalid username or password'})


class SearchView(TemplateView):
    template_name = 'search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query))
        context['query'] = query
        context['products'] = products
        return context


class CheckoutView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **Kwargs):
        context = super().get_context_data(**Kwargs)

        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            current_cart = Cart.objects.get(id=cart_id)
            cart_product = CartProduct.objects.filter(cart=current_cart)
            context['cart_items'] = cart_product
            setTotal(cart_id)
            context['total_price'] = current_cart.total

            # del self.request.session['cart_id']
        return context