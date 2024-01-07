from decimal import Decimal
import decimal
import json

from store.models import Product

class Basket():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket
        
    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = product.id
        
        if product_id not in self.basket:
            discounted_price_str = product.discounted_price()
            discounted_price = float(discounted_price_str.replace(',', ''))
            self.basket[product_id] = {'price': discounted_price, 'qty': int(qty)}

        self.session['basket'] = json.dumps(self.basket)
        self.save()
    
    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['total_price'] = item['price'] * item['qty']
            item['total_price_formatted'] = '{:,.2f}'.format(item['total_price'])
            yield item

        
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        total_price = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        
        formatted_total_price = '{:,.2f}'.format(total_price)
        
        return formatted_total_price

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            print(product_id)
            self.save()
            
    def save(self):
        self.session.modified = True



