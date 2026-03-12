import os
from difflib import SequenceMatcher

class ProductMatcher:
    def __init__(self):
        self.products_db = self.load_product_database()

    def load_product_database(self):
        """Load product database from text file"""
        products = {}
        db_path = "static/products/product_database.txt"

        # Direct URL mapping for specific products
        url_mapping = {
            'zfold5.jpg': {
                'amazon': 'https://www.amazon.in/Samsung-Smartphone-Storage-Powerful-Snapdragon/dp/B0FDL5T1PF',
                'flipkart': 'https://www.flipkart.com/samsung-galaxy-z-fold7-5g-silver-shadow-256-gb/p/itm80780506616fb',
                'snapdeal': 'https://www.snapdeal.com/search?keyword="Samsung+Z+Fold7+5G"'  # optional direct search
            },
            'charger.jpg': {
                'amazon': 'https://www.amazon.in/Ambrane-Charger-Technology-Compatible-Charging/dp/B0CYLKBYG8',
                'flipkart': 'https://www.flipkart.com/ambrane-45-w-gan-3-wall-charger-mobile/p/itmcab45eafb579f',
                'snapdeal': 'https://www.snapdeal.com/search?keyword="Ambrane+45W+charger"'
            },
            'keyboard.jpeg': {
                'amazon': 'https://www.amazon.in/FRONTECH-Multimedia-Ergonomic-Adjustable-KB-1671/dp/B0FMYNZ7VB',
                'flipkart': 'https://www.flipkart.com/rionix-ritro-gaming-key-wired-usb-standard-multi-device-keyboard-compatible-desktop-laptop-tablet/p/itmb66600b43312a',
                'snapdeal': 'https://www.snapdeal.com/product/quantron-black-usb-wired-desktop/638342972479'
            },
            # … other direct mappings …
        }

        if os.path.exists(db_path):
            with open(db_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split('|')
                        if len(parts) == 6:
                            image_name, product_name, description, amazon_price, flipkart_price, snapdeal_price = parts

                            # Use direct URLs if available, otherwise create search URLs
                            if image_name.lower() in url_mapping:
                                urls = url_mapping[image_name.lower()]
                            else:
                                exact_search = f'"{product_name}"'
                                urls = {
                                    'amazon': f'https://www.amazon.in/s?k={exact_search.replace(" ", "+")}&exact=true',
                                    'flipkart': f'https://www.flipkart.com/search?q={exact_search.replace(" ", "%20")}',
                                    'snapdeal': f'https://www.snapdeal.com/search?keyword={exact_search.replace(" ", "+")}'
                                }

                            products[image_name.lower()] = {
                                'name': product_name,
                                'description': description,
                                'amazon': {'price': amazon_price, 'url': urls['amazon']},
                                'flipkart': {'price': flipkart_price, 'url': urls['flipkart']},
                                'snapdeal': {'price': snapdeal_price, 'url': urls['snapdeal']}
                            }

        return products

    def find_matching_product(self, uploaded_filename):
        """Find matching product based on filename similarity"""
        uploaded_name = uploaded_filename.lower()

        # Direct match
        if uploaded_name in self.products_db:
            return self.products_db[uploaded_name]

        # Fuzzy matching
        best_match = None
        best_score = 0

        for db_filename, product_data in self.products_db.items():
            db_name = os.path.splitext(db_filename)[0]
            upload_name = os.path.splitext(uploaded_name)[0]

            similarity = SequenceMatcher(None, upload_name, db_name).ratio()

            product_words = product_data['name'].lower().split()
            for word in product_words:
                if len(word) > 2 and word in upload_name:
                    similarity += 0.4

            if similarity > best_score and similarity > 0.3:
                best_score = similarity
                best_match = product_data

        if not best_match:
            generic_name = uploaded_name.replace("_", " ").replace(".jpg", "").replace(".png", "").replace(".jpeg", "").title()
            exact_search = f'"{generic_name}"'
            best_match = {
                'name': f'{generic_name}',
                'description': f'Search results for {generic_name}',
                'amazon': {
                    'price': 'Check Price',
                    'url': f'https://www.amazon.in/s?k={exact_search.replace(" ", "+")}&exact=true'
                },
                'flipkart': {
                    'price': 'Check Price',
                    'url': f'https://www.flipkart.com/search?q={exact_search.replace(" ", "%20")}'
                },
                'snapdeal': {
                    'price': 'Check Price',
                    'url': f'https://www.snapdeal.com/search?keyword={exact_search.replace(" ", "+")}'
                },
            }

        return best_match

    def get_best_price(self, product_data):
        """Find the store with the lowest price"""
        if not product_data:
            return None

        prices = {}
        for store in ['amazon', 'flipkart', 'snapdeal']:
            price_str = product_data[store]['price']
            numeric_price = ''.join(filter(str.isdigit, price_str.replace(',', '')))
            if numeric_price:
                prices[store] = int(numeric_price)

        if prices:
            best_store = min(prices, key=prices.get)
            return {
                'store': best_store.title(),
                'price': product_data[best_store]['price'],
                'url': product_data[best_store]['url'],
                'savings': max(prices.values()) - min(prices.values())
            }

        return None
