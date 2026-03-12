import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

class PriceScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def setup_driver(self):
        """Setup Chrome driver for Selenium"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
            
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            return driver
        except Exception as e:
            print(f"Error setting up driver: {e}")
            return None
    
    def scrape_amazon(self, product_name):
        """Scrape Amazon for product prices"""
        try:
            driver = self.setup_driver()
            if not driver:
                return {"price": "N/A", "url": ""}
            
            # Search on Amazon
            search_url = f"https://www.amazon.com/s?k={product_name.replace(' ', '+')}"
            driver.get(search_url)
            
            # Wait for results to load
            WebDriverWait(driver, 10).wait(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-component-type="s-search-result"]'))
            )
            
            # Get first product
            products = driver.find_elements(By.CSS_SELECTOR, '[data-component-type="s-search-result"]')
            
            if products:
                first_product = products[0]
                
                # Get price
                price_element = first_product.find_element(By.CSS_SELECTOR, '.a-price-whole, .a-offscreen')
                price = price_element.text if price_element else "N/A"
                
                # Get product URL
                link_element = first_product.find_element(By.CSS_SELECTOR, 'h2 a')
                product_url = "https://www.amazon.com" + link_element.get_attribute('href') if link_element else ""
                
                driver.quit()
                return {"price": f"${price}", "url": product_url}
            
            driver.quit()
            return {"price": "N/A", "url": ""}
            
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            return {"price": "N/A", "url": ""}
    
    def scrape_flipkart(self, product_name):
        """Scrape Flipkart for product prices"""
        try:
            driver = self.setup_driver()
            if not driver:
                return {"price": "N/A", "url": ""}
            
            # Search on Flipkart
            search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '%20')}"
            driver.get(search_url)
            
            # Wait for results
            time.sleep(3)
            
            # Get first product price
            price_elements = driver.find_elements(By.CSS_SELECTOR, '._30jeq3, ._1_WHN1')
            
            if price_elements:
                price = price_elements[0].text
                driver.quit()
                return {"price": price, "url": search_url}
            
            driver.quit()
            return {"price": "N/A", "url": ""}
            
        except Exception as e:
            print(f"Error scraping Flipkart: {e}")
            return {"price": "N/A", "url": ""}
    
    def scrape_snapdeal(self, product_name):
        """Scrape Snapdeal for product prices"""
        try:
            driver = self.setup_driver()
            if not driver:
                return {"price": "N/A", "url": ""}
            
            # Search on Snapdeal
            search_url = f"https://www.snapdeal.com/search?keyword={product_name.replace(' ', '%20')}"
            driver.get(search_url)
            
            # Wait for results
            time.sleep(3)
            
            # Get first product price
            price_elements = driver.find_elements(By.CSS_SELECTOR, '.lfloat.product-price, .product-price')
            
            if price_elements:
                price = price_elements[0].text
                driver.quit()
                return {"price": price, "url": search_url}
            
            driver.quit()
            return {"price": "N/A", "url": ""}
            
        except Exception as e:
            print(f"Error scraping Snapdeal: {e}")
            return {"price": "N/A", "url": ""}
    

    
    def get_all_prices(self, product_name):
        """Get prices from all platforms"""
        print(f"Searching for: {product_name}")
        
        results = {
            "amazon": self.scrape_amazon(product_name),
            "flipkart": self.scrape_flipkart(product_name),
            "snapdeal": self.scrape_snapdeal(product_name)
        }
        
        return results