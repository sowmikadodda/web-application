import os
from difflib import SequenceMatcher
from amazon_handler import AmazonHandler
from flipkart_handler import FlipkartHandler
from snapdeal_handler import SnapdealHandler

class ProductMatcher:
    def __init__(self):
        self.amazon = AmazonHandler()
        self.flipkart = FlipkartHandler()
        self.snapdeal = SnapdealHandler()
        self.products_db = self.load_product_database()
    
    def load_product_database(self):
        """Load product database from text file"""
        products = {}
        db_path = "static/products/product_database.txt"
        
        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as file:
                database_lines = file.readlines()
                
                for line in database_lines:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) == 6:
                            image_name, product_name, description, amazon_price, flipkart_price, snapdeal_price = parts
                            
                            products[image_name.lower()] = {
                                'name': product_name,
                                'description': description,
                                'amazon': {
                                    'price': amazon_price,
                                    'url': self.amazon.get_url(image_name, product_name)
                                },
                                'flipkart': {
                                    'price': flipkart_price,
                                    'url': self.flipkart.get_url(image_name, product_name)
                                },
                                'snapdeal': {
                                    'price': snapdeal_price,
                                    'url': self.snapdeal.get_url(image_name, product_name)
                                }
                            }
        return products
    
    def find_matching_product(self, uploaded_filename):
        """Find matching product based on filename similarity"""
        uploaded_name = uploaded_filename.lower()
        print(f"🔍 Looking for: '{uploaded_name}'")
        print(f"📋 Available keys: {list(self.products_db.keys())}")
        
        # Direct match
        if uploaded_name in self.products_db:
            print(f"✅ Direct match found for: '{uploaded_name}'")
            matched_product = self.products_db[uploaded_name]
            print(f"🔗 Amazon URL: {matched_product['amazon']['url']}")
            print(f"🔗 Flipkart URL: {matched_product['flipkart']['url']}")
            return matched_product
        
        print(f"❌ No exact match found for: '{uploaded_name}'")
        print("Available files: camera.jpeg, charger.jpeg, fan.jpeg, gamepad.jpeg, keyboard.jpeg, kettle.jpeg, laptop.jpeg, mouse.jpeg, tab.jpeg")

        # No fuzzy matching - fallback default values
        generic_name = uploaded_name.replace("_", " ").replace(".jpg", "").replace(".png", "").replace(".jpeg", "").title()

        best_match = {
            'name': 'BrowseBook 14.1\" FHD IPS Laptop',
            'description': 'Best Student & Office Work Laptop | Celeron N4020 | 4GB RAM | 128GB SSD | Windows 11 | 38Wh | 1.3kg | Grey',
            'amazon': {
                'price': 'Rs.12090',
                'url': self.amazon.get_url(uploaded_filename, generic_name)
            },
            'flipkart': {
                'price': 'Rs.9999',
                'url': self.flipkart.get_url(uploaded_filename, generic_name)
            },
            'snapdeal': {
                'price': 'Not Available',
                'url': self.snapdeal.get_url(uploaded_filename, generic_name)
            }
        }
        return best_match
    
    def get_best_price(self, product_data):
        """Find the store with the lowest price or check if prices are equal"""
        if not product_data:
            return None
        
        prices = {}
        for store in ['amazon', 'flipkart', 'snapdeal']:
            price_str = product_data[store]['price']
            # Skip "Not Available" and "Check Price" entries
            if price_str in ['Not Available', 'Check Price']:
                continue
            numeric_price = ''.join(filter(str.isdigit, price_str.replace(',', '')))
            if numeric_price:
                prices[store] = int(numeric_price)
        
        if prices:
            min_price = min(prices.values())
            max_price = max(prices.values())
            
            # Check if prices are equal
            if min_price == max_price:
                return {
                    'store': 'All Stores',
                    'price': product_data['amazon']['price'],
                    'url': '',
                    'savings': 0,
                    'equal_prices': True
                }
            else:
                best_store = min(prices, key=prices.get)
                return {
                    'store': best_store.title(),
                    'price': product_data[best_store]['price'],
                    'url': product_data[best_store]['url'],
                    'savings': max_price - min_price,
                    'equal_prices': False
                }
        
        return None
