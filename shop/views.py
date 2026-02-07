from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, OrderItem
from decimal import Decimal

def index(request):
    return render(request, 'index.html')

def products_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def cart_view(request):
    cart = request.session.get('cart', [])
    total = sum(item['total'] for item in cart)
    return render(request, 'cart.html', {'cart': cart, 'total': total})

@csrf_exempt
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = request.session.get('cart', [])
    
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            item['total'] = float(product.price) * item['quantity']
            break
    else:
        cart.append({
            'product_id': product_id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'total': float(product.price)
        })
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart_view(request)

@csrf_exempt
def create_order(request):
    cart = request.session.get('cart', [])
    
    order = Order.objects.create(
        customer_name=request.POST['customer_name'],
        customer_email=request.POST['customer_email'],
        total=Decimal('0')
    )
    
    total = Decimal('0')
    for item in cart:
        product = Product.objects.get(id=item['product_id'])
        price = product.price * item['quantity']
        total += price
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=price
        )
    
    order.total = total
    order.save()
    
    request.session['cart'] = []
    return render(request, 'order_success.html', {'order': order})
