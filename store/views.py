from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.http import JsonResponse
import json
from django.contrib import messages
# Create your views here.


def index(request):
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        
    context = {"products":products, "cart": cart}
    return render(request, "index.html", context)


def cart(request):
    
    cart = None
    cartitems = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
    
    context = {"cart":cart, "items":cartitems}
    return render(request, "cart.html", context)

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data["id"]
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created =CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        
        
        num_of_item = cart.num_of_items
        
        print(cartitem)
    return JsonResponse(num_of_item, safe=False)


def confirm_payment(request, pk):
    cart = Cart.objects.get(id=pk)
    cart.completed = True
    cart.save()
    messages.success(request, "Payment made successfully")
    return redirect("index")


# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# from django.utils import timezone

# from .models import Cart, CartItem
# from .utils import get_or_create_cart

# @login_required
# @require_POST
# def add_to_cart(request, product_id):
#     cart = get_or_create_cart(request)

#     # Check if the product is already in the cart
#     try:
#         item = cart.cartitem_set.get(product_id=product_id)
#         item.quantity += 1
#         item.save()
#     except CartItem.DoesNotExist:
#         # If the product is not in the cart, create a new cart item
#         product = Product.objects.get(pk=product_id)
#         item = CartItem(cart=cart, product=product, quantity=1)
#         item.save()

#     return redirect('cart:cart_detail')


# def get_or_create_cart(request):
#     if request.user.is_authenticated:
#         # If the user is authenticated, return their cart
#         cart, created = Cart.objects.get_or_create(user=request.user)
#     else:
#         # If the user is not authenticated, get the cart from the session
#         cart_id = request.session.get('cart_id')
#         if cart_id:
#             cart = Cart.objects.filter(id=cart_id).first()
#             if cart is None:
#                 del request.session['cart_id']
#         if cart_id is None or cart is None:
#             # If the cart doesn't exist, create a new cart
#             cart = Cart.objects.create(created=timezone.now())
#             request.session['cart_id'] = cart.id
#     return cart
