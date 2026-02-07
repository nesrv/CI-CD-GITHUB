import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
django.setup()

from shop.models import Product

with open("shop/shop.json", "r", encoding="utf-8") as f:
    products = json.load(f)

Product.objects.all().delete()

for item in products:
    Product.objects.create(
        name=item["name"], price=item["price"], description=item["description"]
    )

print(f"Загружено {len(products)} товаров")
