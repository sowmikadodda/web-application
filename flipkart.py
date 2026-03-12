

import requests
from typing import Dict, List, Optional
import re
from urllib.parse import urlparse, parse_qs, unquote


class FlipkartPriceFetcher:
    def __init__(self, serpapi_key: str):
        self.api_key = serpapi_key
        self.base_url = "https://serpapi.com/search.json"
   
    def extract_flipkart_product_id(self, link: str) -> str:
        """Extract Flipkart product ID from Google Shopping link - Enhanced"""
        try:
            # Direct Flipkart links first
            flipkart_pid_match = re.search(r'pid=([a-zA-Z0-9]{14,})', link)
            if flipkart_pid_match:
                return flipkart_pid_match.group(1)
            
            # Direct path product ID
            path_pid = re.search(r'/([a-zA-Z0-9]{14,})/?', link)
            if path_pid:
                return path_pid.group(1)
            
            # Google Shopping udata params (enhanced patterns)
            parsed = urlparse(link)
            query_params = parse_qs(parsed.query)
            
            if 'udata' in query_params:
                udata = unquote(query_params['udata'][0])
                # Multiple enhanced patterns for Flipkart PID in udata
                pid_patterns = [
                    r'pid=([a-zA-Z0-9]{14,})',
                    r'\/([a-zA-Z0-9]{14,})\?',
                    r'([a-zA-Z0-9]{14,})(?=&|\s|"|\')',
                    r'id=([a-zA-Z0-9]{14,})',
                    r'([a-zA-Z0-9]{14,})(?=\?|\/|&)'
                ]
                for pattern in pid_patterns:
                    match = re.search(pattern, udata, re.IGNORECASE)
                    if match:
                        return match.group(1)
            
            # Check source HTML or other params
            source_match = re.search(r'source=flipkart.*?([a-zA-Z0-9]{14,})', link, re.IGNORECASE)
            if source_match:
                return source_match.group(1)
                
            return ""
        except:
            return ""
    
    def get_flipkart_product_url(self, product_id: str, product_name: str) -> str:
        """Generate direct Flipkart product URL from product ID"""
        if not product_id or len(product_id) < 14:
            # Enhanced search link with exact product name
            safe_query = re.sub(r'[^\w\s]', ' ', product_name).strip()
            encoded_query = '+'.join(safe_query.split())
            return f"https://www.flipkart.com/search?q={encoded_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        return f"https://www.flipkart.com/{product_id}?pid={product_id}"
    
    def fetch_prices(self, query: str, max_results: int = 10) -> List[Dict]:
        params = {
            "engine": "google_shopping",
            "q": f"{query} flipkart",
            "gl": "in",
            "google_domain": "google.co.in",
            "api_key": self.api_key,
            "num": max_results,
            "tbs": "ecom:1"
        }
     
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
         
            products = []
            for product in data.get('shopping_results', []):
                price_data = product.get('price_data', {})
                price_str = product.get('price', '')
             
                price = 0
                if price_data.get('value'):
                    price = float(price_data['value'])
                elif price_str:
                    price_match = re.search(r'₹?([\d,]+\.?\d*)', price_str)
                    if price_match:
                        price = float(price_match.group(1).replace(',', ''))
                
                # CORRECTED RATING EXTRACTION - No hardcoded values
                rating = 0.0
                reviews_count = 0
                
                # Method 1: Direct rating field
                rating_raw = product.get('rating')
                if rating_raw is not None:
                    if isinstance(rating_raw, (int, float)):
                        rating = float(rating_raw)
                    elif isinstance(rating_raw, str) and rating_raw.strip():
                        rating_match = re.search(r'(\d+\.?\d*)', rating_raw)
                        if rating_match:
                            rating = float(rating_match.group(1))
                
                # Method 2: reviews field
                reviews_raw = product.get('reviews')
                if reviews_raw and rating == 0.0:
                    if isinstance(reviews_raw, str):
                        # "4.6 (123 ratings)" format
                        combined_match = re.search(r'(\d+\.?\d*)\s*\(?\s*(\d+)', reviews_raw)
                        if combined_match:
                            rating = float(combined_match.group(1))
                            reviews_count = int(combined_match.group(2))
                
                # Method 3: reviews_count field
                reviews_count_raw = product.get('reviews_count')
                if reviews_count_raw:
                    reviews_count = int(reviews_count_raw) if isinstance(reviews_count_raw, (int, str)) else 0
                
                # Extract shipping info
                shipping = "Free Shipping" if product.get('shipping') else "Check Shipping"
                delivery = product.get('delivery', shipping)
                
                link = product.get('link', '')
                product_name = product.get('title', '')[:80]
                
                # Enhanced link extraction
                product_id = self.extract_flipkart_product_id(link)
                flipkart_link = self.get_flipkart_product_url(product_id, product_name)
                
                if price > 0:
                    products.append({
                        'price': price,
                        'link': flipkart_link,
                        'name': product_name,
                        'rating': rating,
                        'shipping': delivery or shipping,
                        'reviews': reviews_count,
                        'product_id': product_id
                    })
            
            # Sort by price (lowest first)
            products.sort(key=lambda x: x['price'])
            return products
        except Exception as e:
            print(f"Error: {e}")
            return []
   
    def get_lowest_price(self, query: str, max_results: int = 10) -> Optional[Dict]:
        products = self.fetch_prices(query, max_results)
        return products[0] if products else None
   
    def print_lowest_price(self, query: str, max_results: int = 10):
        lowest = self.get_lowest_price(query, max_results)
        if not lowest:
            print("❌ No Flipkart products found.")
            return
        
        direct_link = lowest['link']
        
        print(f"\n🏆 LOWEST FLIPKART DEAL FOUND!")
        print(f"   💰 Price: ₹{lowest['price']:,.0f}")
        # FIXED: Uses ACTUAL extracted rating, no hardcoded values!
        if lowest['rating'] > 0:
            print(f"   ⭐ Rating: {lowest['rating']:.1f} ({int(lowest['reviews'])} reviews)")
        else:
            print(f"   ⭐ Rating: Not available ({int(lowest['reviews'])} reviews)")
        print(f"   🚚 Shipping: {lowest['shipping']}")
        print(f"   📱 Buy Now: {direct_link}")
        print(f"   📦 Product: {lowest['name']}")
        print("\n" + "="*60)


# USAGE - Same as before
if __name__ == "__main__":
    API_KEY = "API_KEY"
   
    fetcher = FlipkartPriceFetcher(API_KEY)
   
    product_name = input("Enter product name (or 'refrigerator' for test): ").strip()
    if not product_name:
        product_name = "refrigerator under 10000"
   
    print(f"🔍 Searching Flipkart: {product_name}")
    fetcher.print_lowest_price(product_name)


