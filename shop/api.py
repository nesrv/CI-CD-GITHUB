from ninja import NinjaAPI, Schema
from django.shortcuts import get_object_or_404
from .models import Product, Order, OrderItem
from typing import List
from decimal import Decimal
from datetime import datetime

api = NinjaAPI()

class ProductSchema(Schema):
    id: int
    name: str
    price: float
    description: str

class OrderCreateSchema(Schema):
    customer_name: str
    customer_email: str
    items: List[dict]

class OrderSchema(Schema):
    id: int
    customer_name: str
    customer_email: str
    total: float
    created_at: datetime

@api.get("/products", response=List[ProductSchema])
def list_products(request):
    return Product.objects.all()

@api.get("/products/{product_id}", response=ProductSchema)
def get_product(request, product_id: int):
    return get_object_or_404(Product, id=product_id)

@api.post("/orders", response=OrderSchema)
def create_order(request, order_data: OrderCreateSchema):
    total = Decimal('0')
    order = Order.objects.create(
        customer_name=order_data.customer_name,
        customer_email=order_data.customer_email,
        total=total
    )
    
    for item_data in order_data.items:
        product = get_object_or_404(Product, id=item_data['product_id'])
        quantity = item_data['quantity']
        price = product.price * quantity
        total += price
        
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )
    
    order.total = total
    order.save()
    return order

@api.get("/orders", response=List[OrderSchema])
def list_orders(request):
    return Order.objects.all()

@api.get("/health")
def health_check(request):
    return {"status": "ok"}