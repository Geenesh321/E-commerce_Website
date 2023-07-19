from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, default=None)  
    email = models.EmailField( default=None)  
    phone = models.CharField(max_length=20 , default=None) 
    address = models.CharField(max_length=150, null=True, default=None)
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100 , default=None)  
    country = models.CharField(max_length=100 , default=None)  
    pin_code = models.CharField(max_length=10 , default=None)  
    joined_on = models.DateTimeField(auto_now_add=True)


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    
class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    image = models.ImageField(upload_to='product', default='None')
    marked_priced = models.PositiveBigIntegerField()
    selling_price = models.PositiveBigIntegerField()
    description = models.TextField()
    warrenty = models.CharField(max_length=50)
    return_policy = models.CharField(max_length=150)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True ) 
    total = models.PositiveIntegerField()
    created_cart = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart:" + str(self.id)

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField()

    def __str__(Self):
        return "Cart: " + str(Self.id) + "CartProduct: " + str(Self.id)

ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("Order On the Way", "Order On the Way"),
    ("Order Complete", "Order Complete"),
)

class Order(models.Model):
    Cart= models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=150)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    sub_total = models.PositiveBigIntegerField()
    discount = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    order_status = models.CharField(max_length=150, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

class BasicDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"