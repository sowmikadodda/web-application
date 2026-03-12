# import requests
# import json
# import logging
# import re
# from typing import Dict, List, Optional
# from urllib.parse import quote_plus

# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

# class SerpApiAmazonScraper:
#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.base_url = "https://serpapi.com/search.json"
        
#         self.product_synonyms = {
#             'refrigerator': ['mini refrigerator','mini fridge','fridge', 'refrigerator', 'single door fridge', 'double door fridge'],
#             'electric fan': ['fan', 'ceiling fan', 'pedestal fan', 'wall fan', 'table fan'],
#             'iphone': ['iphone', 'apple iphone'],
#             'samsung galaxy': ['samsung galaxy', 'galaxy s', 'samsung s'],
#             'backpack': ['backpack', 'rucksack', 'school bag', 'laptop bag','bag'],
#             'television': ['tv', 'television', 'led tv', 'smart tv'],
#             'washing machine': ['washing machine', 'washer'],
#             'air conditioner': ['ac', 'air conditioner', 'split ac', 'window ac'],
#             'jean': ['women jeans','jeans','baggy jeans','straight jeans', 'denim jeans'],
#             'running shoes': ['shoes','shoe','sneakers', 'running shoes', 'sports shoes', 'athletic shoes', 'trainers']  # ✅ FIXED: Added variations
#         }

#     def get_search_variations(self, product_name: str) -> List[str]:
#         """Generate multiple search variations using synonyms"""
#         product_lower = product_name.lower()
#         variations = [product_name]
        
#         # ✅ FIXED: Check for exact key match OR any word from key
#         for key, synonyms in self.product_synonyms.items():
#             # Check if key OR any word from key exists in product
#             key_words = key.lower().split()
#             if any(word in product_lower for word in key_words) or key in product_lower:
#                 variations.extend(synonyms)
#                 logger.info(f"✅ Found synonym match for '{key}' → adding {len(synonyms)} variations")
#                 break
        
#         # Add space-removed variation
#         variations.append(product_name.replace(' ', '').replace('_', ''))
        
#         # Remove duplicates and limit
#         variations = list(dict.fromkeys(variations))[:6]  # 6 variations max
#         logger.info(f"🔍 FINAL variations for '{product_name}': {variations}")
#         return variations

#     def get_price_ranges(self, product_name: str) -> tuple:
#         """Dynamic realistic price ranges"""
#         product_lower = product_name.lower()
        
#         # ✅ FIXED: Use split() to match individual words (handles underscores/spaces)
#         product_words = product_lower.replace('_', ' ').split()
        
#         if any(word in product_words for word in ['fridge', 'refrigerator']):
#             return 7000, 100000
#         elif any(word in product_words for word in ['samsung', 'galaxy', 's24']):
#             return 8000, 100000
#         elif any(word in product_words for word in ['fan', 'electric', 'fan']):
#             return 800, 8000
#         elif any(word in product_words for word in ['jean', 'jeans']):
#             return 100, 5000
#         elif any(word in product_words for word in ['running', 'shoes', 'shoe', 'sneakers']):  # ✅ FIXED: Split matching
#             return 200, 8000  # Increased upper limit for better results
#         elif 'backpack' in product_words:
#             return 100, 5000
#         else:
#             return 100, 100000

#     def is_main_product(self, title: str, product_name: str) -> bool:
#         """Smart main product detection with synonyms"""
#         title_lower = title.lower()
#         product_lower = product_name.lower()
        
#         # Block obvious accessories
#         blocks = ['case', 'cover', 'charger', 'cable', 'screen protector',
#                 'tempered glass', 'luggage cover', 'armour', 'polycarbonate',
#                 'sock', 'belt', 'wallet']  # Added more blocks
        
#         if any(block in title_lower for block in blocks):
#             return False
        
#         # Get matching synonyms for better detection
#         matching_synonyms = []
#         product_words = product_lower.replace('_', ' ').split()
        
#         for key, synonyms in self.product_synonyms.items():
#             key_words = key.lower().split()
#             if any(word in product_words for word in key_words):
#                 matching_synonyms.extend(synonyms)
#                 break
        
#         # Keywords from product name + synonyms
#         keywords = list(set(product_words + matching_synonyms))
#         keywords = [w for w in keywords if len(w) > 2]
        
#         # Require at least 50% keyword match OR minimum 1 match
#         matches = sum(1 for k in keywords if k in title_lower)
#         match_ratio = matches / len(keywords) if keywords else 0
        
#         logger.debug(f"Title: '{title[:50]}...' | Keywords: {keywords} | Matches: {matches}/{len(keywords)}")
    
#         return matches >= 1 and (match_ratio >= 0.4 or 'shoes' in title_lower or 'sneakers' in title_lower)

    
#     def create_redirect_link(self, link: str, asin: str = None) -> str:
#         if not link:
#             return ""
#         if asin:
#             return f"https://www.amazon.in/dp/{asin}?tag=yourtag-21&linkCode=ogi&th=1&psc=1"
#         redirect_link = link
#         if "amazon.in" in link:
#             redirect_link += "&tag=yourtag-21&linkCode=ll1"
#         return redirect_link
    
#     def get_lowest_price(self, product_name: str, max_results: int = 50) -> Optional[Dict]:
#         all_valid_products = []
#         search_variations = self.get_search_variations(product_name)
        
#         for variation in search_variations:
#             params = {
#                 "engine": "amazon",
#                 "k": variation,
#                 "api_key": self.api_key,
#                 "amazon_domain": "amazon.in",
#                 "sort_by": "price-asc-rank",
#                 "page_size": max_results // len(search_variations),
#                 "location": "India"
#             }
            
#             try:
#                 response = requests.get(self.base_url, params=params, timeout=15)
#                 data = response.json()
#                 results = data.get("organic_results", [])
                
#                 min_price, max_price = self.get_price_ranges(variation)
#                 variation_products = []
                
#                 for result in results:
#                     title = result.get("title", "")
#                     if not self.is_main_product(title, product_name):
#                         continue
                    
#                     price_str = result.get("price") or result.get("extracted_price")
#                     if not price_str or '₹' not in str(price_str):
#                         continue
                    
#                     price_clean = re.sub(r'[₹,\s]', '', str(price_str))
#                     price_match = re.search(r'[\d]+\.?\d*', price_clean)
                    
#                     if price_match:
#                         price_num = float(price_match.group())
#                         if min_price <= price_num <= max_price:
#                             redirect_link = self.create_redirect_link(
#                                 result.get("link"), 
#                                 result.get("asin")
#                             )
                            
#                             variation_products.append({
#                                 'result': result,
#                                 'price': price_num,
#                                 'title': title,
#                                 'search_term': variation,
#                                 'redirect_link': redirect_link
#                             })
                
#                 all_valid_products.extend(variation_products)
#                 logger.info(f"Variation '{variation}': {len(variation_products)} products")
                
#             except Exception as e:
#                 logger.warning(f"Variation '{variation}' failed: {e}")
#                 continue
        
#         if not all_valid_products:
#             return None
        
#         all_valid_products.sort(key=lambda x: x['price'])
#         true_lowest = all_valid_products[0]
        
#         logger.info(f"✅ FINAL LOWEST: ₹{true_lowest['price']:,} from '{true_lowest['search_term']}'")
        
#         result_data = true_lowest['result']
#         delivery_info = result_data.get('delivery', 'Check page')
#         is_prime = "Prime" in result_data.get('title', '') or result_data.get('is_prime') or "Prime" in delivery_info
        
#         return {
#             "lowest_price": f"₹{true_lowest['price']:,.0f}",
#             "price_value": true_lowest['price'],
#             "title": result_data.get("title", ""),
#             "link": true_lowest['result'].get("link"),
#             "redirect_link": true_lowest['redirect_link'],
#             "asin": result_data.get("asin"),
#             "rating": result_data.get("rating", 0),
#             "reviews": result_data.get("reviews", 0),
#             "thumbnail": result_data.get("thumbnail"),
#             "delivery": delivery_info,
#             "is_prime": is_prime,
#             "total_checked": len(all_valid_products),
#             "search_variations": len(search_variations),
#             "best_search_term": true_lowest['search_term']
#         }

# def get_amazon_price(product_name: str, serpapi_key: str = "913baa38df89f798c36d1060941926131a709a8bfa44a2247f47d6dd21e1de17") -> Dict[str, any]:
#     """
#     MAIN FUNCTION for app.py - Returns ALL product details as dict
#     """
#     try:
#         scraper = SerpApiAmazonScraper(serpapi_key)
#         result = scraper.get_lowest_price(product_name)
        
#         if result:
#             return {
#                 "success": True,
#                 "price": result["lowest_price"],
#                 "price_value": result["price_value"],
#                 "title": result["title"][:100],
#                 "link": result["redirect_link"],
#                 "asin": result["asin"],
#                 "rating": f"{result['rating']}/5" if result["rating"] else "N/A",
#                 "reviews": f"{result['reviews']:,}" if result["reviews"] else "0",
#                 "delivery": "Prime" if result["is_prime"] else result.get("delivery", "Standard"),
#                 "image": result["thumbnail"],
#                 "total_checked": result["total_checked"],
#                 "search_term": result["best_search_term"]
#             }
#         else:
#             return {
#                 "success": False,
#                 "price": "No products found",
#                 "link": "https://www.amazon.in",
#                 "title": product_name,
#                 "rating": "N/A",
#                 "reviews": "0",
#                 "delivery": "N/A",
#                 "image": "",
#                 "total_checked": 0
#             }
#     except Exception as e:
#         logger.error(f"Amazon scrape failed for {product_name}: {e}")
#         return {
#             "success": False,
#             "price": f"❌ Error: {str(e)[:50]}",
#             "link": "",
#             "title": product_name,
#             "rating": "N/A",
#             "reviews": "0",
#             "delivery": "N/A",
#             "image": "",
#             "total_checked": 0
#         }

# if __name__ == "__main__":
#     API_KEY = "913baa38df89f798c36d1060941926131a709a8bfa44a2247f47d6dd21e1de17"
#     result = get_amazon_price("refrigerator")
#     print(json.dumps(result, indent=2))


import requests
import json
import logging
import re
from typing import Dict, List, Optional
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class SerpApiAmazonScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search.json"
        
        self.product_synonyms = {
            'refrigerator': ['fridge', 'refrigerator', 'single door fridge', 'double door fridge'],
            'electric fan': ['fan', 'ceiling fan', 'pedestal fan', 'wall fan', 'table fan'],
            'iphone': ['iphone', 'apple iphone'],
            'samsung galaxy': ['samsung galaxy', 'galaxy s', 'samsung s'],
            'backpack': ['backpack', 'rucksack', 'school bag', 'laptop bag','bag'],
            'television': ['tv', 'television', 'led tv', 'smart tv'],
            'washing machine': ['washing machine', 'washer'],
            'air conditioner': ['ac', 'air conditioner', 'split ac', 'window ac'],
            'jean': ['women jeans','jeans','baggy jeans','straight jeans', 'denim jeans'],
            'running shoes': ['shoes','shoe','sneakers', 'running shoes', 'sports shoes', 'athletic shoes', 'trainers']
        }

    def get_search_variations(self, product_name: str) -> List[str]:
        """Generate multiple search variations using synonyms"""
        product_lower = product_name.lower()
        variations = [product_name]
        
        for key, synonyms in self.product_synonyms.items():
            key_words = key.lower().split()
            if any(word in product_lower for word in key_words) or key in product_lower:
                variations.extend(synonyms)
                logger.info(f"✅ Found synonym match for '{key}' → adding {len(synonyms)} variations")
                break
        
        variations.append(product_name.replace(' ', '').replace('_', ''))
        variations = list(dict.fromkeys(variations))[:6]
        logger.info(f"🔍 FINAL variations for '{product_name}': {variations}")
        return variations

    def get_price_ranges(self, product_name: str) -> tuple:
        """Dynamic realistic price ranges"""
        product_lower = product_name.lower()
        product_words = product_lower.replace('_', ' ').split()
        
        if any(word in product_words for word in ['fridge', 'refrigerator']):
            return 7000, 100000
        elif any(word in product_words for word in ['samsung', 'galaxy', 's24']):
            return 8000, 100000
        elif any(word in product_words for word in ['fan', 'electric', 'fan']):
            return 800, 8000
        elif any(word in product_words for word in ['jean', 'jeans']):
            return 100, 5000
        elif any(word in product_words for word in ['running', 'shoes', 'shoe', 'sneakers']):
            return 200, 8000
        elif 'backpack' in product_words:
            return 100, 5000
        else:
            return 100, 100000

    def is_main_product(self, title: str, product_name: str) -> bool:
        """Smart main product detection with synonyms"""
        title_lower = title.lower()
        product_lower = product_name.lower()
        
        blocks = ['case', 'cover', 'charger', 'cable', 'screen protector',
                'tempered glass', 'luggage cover', 'armour', 'polycarbonate',
                'sock', 'belt', 'wallet']
        
        if any(block in title_lower for block in blocks):
            return False
        
        matching_synonyms = []
        product_words = product_lower.replace('_', ' ').split()
        
        for key, synonyms in self.product_synonyms.items():
            key_words = key.lower().split()
            if any(word in product_words for word in key_words):
                matching_synonyms.extend(synonyms)
                break
        
        keywords = list(set(product_words + matching_synonyms))
        keywords = [w for w in keywords if len(w) > 2]
        
        matches = sum(1 for k in keywords if k in title_lower)
        match_ratio = matches / len(keywords) if keywords else 0
        
        logger.debug(f"Title: '{title[:50]}...' | Keywords: {keywords} | Matches: {matches}/{len(keywords)}")
    
        return matches >= 1 and (match_ratio >= 0.4 or 'shoes' in title_lower or 'sneakers' in title_lower)

    
    def create_redirect_link(self, link: str, asin: str = None) -> str:
        if not link:
            return ""
        if asin:
            return f"https://www.amazon.in/dp/{asin}?tag=yourtag-21&linkCode=ogi&th=1&psc=1"
        redirect_link = link
        if "amazon.in" in link:
            redirect_link += "&tag=yourtag-21&linkCode=ll1"
        return redirect_link
    
    def get_lowest_price(self, product_name: str, max_results: int = 50) -> Optional[Dict]:
        all_valid_products = []
        search_variations = self.get_search_variations(product_name)
        
        for variation in search_variations:
            params = {
                "engine": "amazon",
                "k": variation,
                "api_key": self.api_key,
                "amazon_domain": "amazon.in",
                "sort_by": "price-asc-rank",
                "page_size": max_results // len(search_variations),
                "location": "India"
            }
            
            try:
                response = requests.get(self.base_url, params=params, timeout=15)
                data = response.json()
                results = data.get("organic_results", [])
                
                min_price, max_price = self.get_price_ranges(variation)
                variation_products = []
                
                for result in results:
                    title = result.get("title", "")
                    if not self.is_main_product(title, product_name):
                        continue
                    
                    price_str = result.get("price") or result.get("extracted_price")
                    if not price_str or '₹' not in str(price_str):
                        continue
                    
                    price_clean = re.sub(r'[₹,\s]', '', str(price_str))
                    price_match = re.search(r'[\d]+\.?\d*', price_clean)
                    
                    if price_match:
                        price_num = float(price_match.group())
                        if min_price <= price_num <= max_price:
                            redirect_link = self.create_redirect_link(
                                result.get("link"), 
                                result.get("asin")
                            )
                            
                            variation_products.append({
                                'result': result,
                                'price': price_num,
                                'title': title,
                                'search_term': variation,
                                'redirect_link': redirect_link
                            })
                
                all_valid_products.extend(variation_products)
                logger.info(f"Variation '{variation}': {len(variation_products)} products")
                
            except Exception as e:
                logger.warning(f"Variation '{variation}' failed: {e}")
                continue
        
        if not all_valid_products:
            return None
        
        all_valid_products.sort(key=lambda x: x['price'])
        true_lowest = all_valid_products[0]
        
        logger.info(f"✅ FINAL LOWEST: ₹{true_lowest['price']:,} from '{true_lowest['search_term']}'")
        
        result_data = true_lowest['result']
        
        # --- FIX: Handle Delivery being a List or String ---
        delivery_raw = result_data.get('delivery')
        if isinstance(delivery_raw, list):
            delivery_info = " ".join(delivery_raw) # Join list items into one string
        else:
            delivery_info = str(delivery_raw) if delivery_raw else "Check delivery date on page"
            
        is_prime = "Prime" in result_data.get('title', '') or result_data.get('is_prime') or "Prime" in delivery_info
        
        return {
            "lowest_price": f"₹{true_lowest['price']:,.0f}",
            "price_value": true_lowest['price'],
            "title": result_data.get("title", ""),
            "link": true_lowest['result'].get("link"),
            "redirect_link": true_lowest['redirect_link'],
            "asin": result_data.get("asin"),
            "rating": result_data.get("rating"), # Get raw rating (can be None)
            "reviews": result_data.get("reviews"), # Get raw reviews (can be None)
            "thumbnail": result_data.get("thumbnail"),
            "delivery": delivery_info, 
            "is_prime": is_prime,
            "total_checked": len(all_valid_products),
            "search_variations": len(search_variations),
            "best_search_term": true_lowest['search_term']
        }

def get_amazon_price(product_name: str, serpapi_key: str = "API_KEY") -> Dict[str, any]:
    """
    MAIN FUNCTION for app.py - Returns ALL product details as dict
    """
    try:
        scraper = SerpApiAmazonScraper(serpapi_key)
        result = scraper.get_lowest_price(product_name)
        
        if result:
            # Format Delivery Text
            delivery_text = result["delivery"]
            if result["is_prime"] and "Prime" not in str(delivery_text):
                delivery_text = f"{delivery_text} (Prime)"
            
            # Safe formatting for Rating and Reviews
            rating_val = result.get("rating")
            reviews_val = result.get("reviews")
            
            return {
                "success": True,
                "price": result["lowest_price"],
                "price_value": result["price_value"],
                "title": result["title"][:100],
                "link": result["redirect_link"],
                "asin": result["asin"],
                # Fix: Handle None types safely for rating/reviews
                "rating": f"{rating_val}" if rating_val else "N/A",
                "reviews": f"{reviews_val:,}" if isinstance(reviews_val, (int, float)) else "0",
                "delivery": delivery_text,
                "image": result["thumbnail"],
                "total_checked": result["total_checked"],
                "search_term": result["best_search_term"]
            }
        else:
            return {
                "success": False,
                "price": "No products found",
                "link": "https://www.amazon.in",
                "title": product_name,
                "rating": "N/A",
                "reviews": "0",
                "delivery": "N/A",
                "image": "",
                "total_checked": 0
            }
    except Exception as e:
        logger.error(f"Amazon scrape failed for {product_name}: {e}")
        return {
            "success": False,
            "price": f"❌ Error: {str(e)[:50]}",
            "link": "",
            "title": product_name,
            "rating": "N/A",
            "reviews": "0",
            "delivery": "N/A",
            "image": "",
            "total_checked": 0
        }
if __name__ == "__main__":
    API_KEY = "API_KEY"
    result = get_amazon_price("refrigerator")
    print(json.dumps(result, indent=2))