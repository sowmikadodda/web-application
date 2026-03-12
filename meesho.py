from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

def extract_title_from_meesho_url(link: str) -> str:
    """Extract product title from Meesho URL slug"""
    try:
        parsed = urlparse(link)
        path = parsed.path
        slug = path.split('/p/')[0].strip('/')
        if slug:
            return slug.replace('-', ' ').title()[:100]
        return "Meesho Product"
    except:
        return "Meesho Product"

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    return driver

def get_product_title_from_page(product_url: str) -> str:
    """Fetch the exact PDP title (h1/h2) for the product."""
    driver = setup_driver()
    try:
        driver.get(product_url)
        time.sleep(4)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        title_elem = (
            soup.find("h1")
            or soup.find("h2")
            or soup.find("p", class_=re.compile(r"title|name|product", re.I))
        )
        if title_elem:
            return title_elem.get_text(strip=True)[:120]
        return "Meesho Product"
    finally:
        driver.quit()

def scrape_meesho_lowest_price(product_name: str):
    """Meesho search: title + rating (1 decimal) + reviews (after comma) + price + link."""

    driver = setup_driver()

    try:
        print(f"🔍 Searching Meesho: {product_name}")
        url = f"https://www.meesho.com/search?q={product_name}"
        print(f"📱 URL: {url}")

        driver.get(url)
        time.sleep(4)

        products = []

        product_elements = driver.find_elements(
            By.CSS_SELECTOR,
            "[data-testid='product-card'], .product, [class*='product'], [class*='card'], a[href*='/p/']"
        )

        for elem in product_elements[:15]:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", elem)
                time.sleep(0.3)

                elem_html = BeautifulSoup(elem.get_attribute("outerHTML"), "html.parser")

                # ---------- TITLE (temporary from card) ----------
                title = "Meesho Product"

                # 1) Prefer headings with product-name-like classes
                title_elem = elem_html.find(
                    ["h3", "h4", "h5", "h6"],
                    class_=re.compile(r"(product|title|name)", re.I)
                )

                # 2) Fallback: any tag with product/title/name in class
                if not title_elem:
                    title_elem = elem_html.find(
                        True,
                        class_=re.compile(r"(product|title|name)", re.I)
                    )

                # 3) Last fallback: a longer text node, but avoid one-word things like "mouse"
                if not title_elem:
                    candidate = elem_html.find(
                        string=lambda x: x
                        and len(x.strip()) > 10     # avoid single words
                        and len(x.strip()) < 150
                    )
                    if candidate:
                        title_elem = candidate

                # Normalize
                if title_elem:
                    if hasattr(title_elem, "get_text"):
                        title_text = title_elem.get_text(strip=True)
                    else:
                        title_text = str(title_elem).strip()

                    # Extra guard: if still too short / generic, keep default
                    if len(title_text) > 10:
                        title = title_text[:100]

                # ---------- PRICE ----------
                price_elem = elem_html.find(lambda tag: tag and "₹" in tag.get_text())
                if not price_elem:
                    continue

                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r"₹([\d,]+\.?\d*)", price_text)
                if not price_match:
                    continue

                price_num = float(price_match.group(1).replace(",", ""))

                # ---------- RATING & REVIEWS ----------
                rating = "N/A"
                reviews = "N/A"

                rating_block = (
                    elem_html.find(
                        string=re.compile(r"\d+\.?\d*\s*(⭐|★|star|rating)", re.I)
                    )
                    or elem_html.find(
                        attrs={"class": re.compile(r"rating", re.I)}
                    )
                )

                if rating_block:
                    if hasattr(rating_block, "get_text"):
                        rating_text = rating_block.get_text(strip=True)
                    else:
                        rating_text = str(rating_block).strip()

                    # first number = rating
                    rating_match = re.search(r"(\d+\.?\d*)", rating_text)
                    if rating_match:
                        rating_value = float(rating_match.group(1))
                        rating = f"{rating_value:.1f}"  # one digit after decimal

                    # reviews like "4.0 ★ 2188 Ratings, 1994 Reviews"
                    reviews = "N/A"
                    reviews_match = re.search(
                        r"Ratings,\s*(\d[\d,]*)\s+Reviews", rating_text, re.I
                    )
                    if reviews_match:
                        reviews = reviews_match.group(1).replace(",", "")

                # ---------- DELIVERY (from search card) ----------
                delivery = "N/A"
                delivery_elem = (
                    elem_html.find(string=re.compile(r"Free Delivery", re.I))
                    or elem_html.find(attrs={"class": re.compile(r"delivery", re.I)})
                )
                if delivery_elem:
                    if hasattr(delivery_elem, "get_text"):
                        delivery = delivery_elem.get_text(strip=True)
                    else:
                        delivery = str(delivery_elem).strip()

                # ---------- LINK ----------
                link_elem = elem_html.find("a", href=True)
                if not link_elem or "/p/" not in link_elem["href"]:
                    continue

                link = urljoin("https://www.meesho.com", link_elem["href"])

                # ✅ TITLE FROM URL SLUG
                final_title = extract_title_from_meesho_url(link)

                products.append(
                    {
                        "name": final_title,
                        "rating": rating,
                        "reviews": reviews,
                        "price": f"₹{price_match.group(1)}",
                        "price_num": price_num,
                        "link": link,
                    }
                )

            except Exception:
                continue

        driver.quit()

        if not products:
            print("❌ No products found")
            return None

        # ✅ FIXED: Filter + Relevance Scoring
        def is_relevant_product(title_lower, search_lower):
            exclude_words = ['pad', 'mat', 'cover', 'skin', 'sticker', 'protector', 'sheet']
            if any(word in title_lower for word in exclude_words):
                return False
            return search_lower in title_lower or any(w in title_lower for w in search_lower.split()[:2])

        # Filter out keyboard pads first
        relevant_products = [p for p in products if is_relevant_product(p['name'].lower(), product_name.lower())]
        
        if not relevant_products:
            relevant_products = products  # Fallback if no perfect matches

        def relevance_score(title_lower, search_lower):
            score = 0
            if search_lower in title_lower:
                score += 200
            elif any(w in title_lower for w in search_lower.split()):
                score += 100
            return score

        # Sort: price first, then relevance
        sorted_products = sorted(relevant_products, key=lambda x: (x['price_num'], -relevance_score(x['name'].lower(), product_name.lower())))
        lowest = sorted_products[0]

        print("\n" + "=" * 70)
        print("🏆 MEEsHO LOWEST PRICE")
        print("=" * 70)
        print(f"📦 {lowest['name']}")
        print(f"⭐ {lowest['rating']}")
        print(f"📝 Reviews: {lowest['reviews']}")
        print(f"🚚 Free Delivery")
        print(f"💰 {lowest['price']}")
        print(f"🔗 {lowest['link']}")
        print(f"🎯 Checked {len(products)} products")
        print("=" * 70)

        lowest["delivery"] = "Free Delivery"
        return lowest

    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    product = input("Enter product (or Enter for test): ").strip()
    if not product:
        product = "mouse"
    scrape_meesho_lowest_price(product)
