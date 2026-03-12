
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

def extract_price(text):
    """Cleans text to return a float price."""
    if not text:
        return None
    m = re.search(r'[\d,]+', text)
    if not m:
        return None
    return float(m.group(0).replace(',', ''))

def extract_reviews(text):
    """Extracts number from '(123)' format."""
    if not text:
        return "0"
    m = re.search(r'(\d+)', text)
    return m.group(1) if m else "0"

def get_snapdeal_lowest_price(product_name):
    options = Options()
    options.add_argument("--headless=new") 
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Sort by Price Low to High
    url = f"https://www.snapdeal.com/search?keyword={product_name}&sort=plth"
    
    print(f"Searching Snapdeal for: {product_name}...")
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    products = []

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-tuple-listing")))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.product-tuple-listing")

        for card in cards:
            try:
                # 1. Link & Title
                link_el = card.find_element(By.CSS_SELECTOR, "a.dp-widget-link")
                link = link_el.get_attribute("href")
                # Try getting title from paragraph tag if attribute is missing
                try:
                    title = card.find_element(By.CSS_SELECTOR, "p.product-title").text
                except:
                    title = link_el.get_attribute("title")

                # 2. Price
                price_el = card.find_element(By.CSS_SELECTOR, "span.lfloat.product-price")
                price = extract_price(price_el.text)

                if price is None:
                    continue

                # 3. Rating (Calculated from Star Width)
                rating = "N/A"
                try:
                    # Snapdeal shows rating as width % (e.g. width: 80% = 4 stars)
                    star_el = card.find_element(By.CSS_SELECTOR, "div.filled-stars")
                    width_style = star_el.get_attribute("style") 
                    # Extract number from "width: 90.0%"
                    width_val = re.search(r'([\d\.]+)', width_style)
                    if width_val:
                        percentage = float(width_val.group(1))
                        rating = round((percentage / 20), 1) # Convert % to 5-star scale
                except:
                    pass

                # 4. Reviews
                reviews = "0"
                try:
                    review_el = card.find_element(By.CSS_SELECTOR, "p.product-rating-count")
                    reviews = extract_reviews(review_el.text)
                except:
                    pass

                # 5. Delivery (Search page usually doesn't show date, checking for badges)
                delivery = "Check details at link" 
                # Sometimes Snapdeal shows "Free Delivery" on the card
                if "Free Delivery" in card.text:
                    delivery = "Free Delivery (Date depends on Pincode)"

                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "delivery": delivery,
                    "link": link
                })

            except Exception:
                continue

    except Exception as e:
        print(f"Error scraping Snapdeal: {e}")
    finally:
        driver.quit()

    if not products:
        return None

    # Sort by price (Low to High)
    products.sort(key=lambda x: x["price"])
    return products[0]

def get_snapdeal_price(product_name):
    result = get_snapdeal_lowest_price(product_name)

    if not result:
        return {
            "success": False,
            "price": "No products found",
            "link": f"https://www.snapdeal.com/search?keyword={product_name}"
        }

    return {
        "success": True,
        "price": f"₹{int(result['price'])}",
        "price_value": result["price"],
        "title": result["title"],
        "rating": result["rating"],
        "reviews": result["reviews"],
        "delivery": result["delivery"],
        "link": result["link"]
    }

# --- TEST BLOCK ---
if __name__ == "__main__":
    item = "mouse"
    data = get_snapdeal_price(item)
    
    if data["success"]:
        print(f"✅ Found Cheapest '{item}':")
        print(f"Title:    {data['title']}")
        print(f"Price:    {data['price']}")
        print(f"Rating:   {data['rating']} stars")
        print(f"Reviews:  {data['reviews']}")
        print(f"Delivery: {data['delivery']}")
        print(f"Link:     {data['link']}")
    else:
        print("❌ Product not found.")
