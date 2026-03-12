class SnapdealHandler:
    def __init__(self):
        self.base_url = "https://www.snapdeal.com"
        
    def get_product_urls(self):
        """Snapdeal product URLs mapping"""
        return {
            'earbuds.jpeg': 'https://www.snapdeal.com/product/wireless-tws-earbuds-with-5/666059881112#bcrumbSearch:earbud%20under%20250',
            'charger.jpeg': 'https://www.snapdeal.com/product/portronics-no-cable-24a-wall/640340478189',
            'fan.jpeg': 'https://www.snapdeal.com/product/crompton-ceiling-fan/123456796',
            'gamepad.jpeg': 'https://www.snapdeal.com/product/500-in-1-controller-gamepad/633780712654',
            'keyboard.jpeg': 'https://www.snapdeal.com/product/quantron-black-usb-wired-desktop/638342972479',
            'kettle.jpeg': 'https://www.snapdeal.com/product/scarlett-silver-18-litres-stainless/642310272446#bcrumbSearch:kettle',
            'laptop.jpeg': 'https://www.snapdeal.com/search?keyword=laptop',
            'mouse.jpeg': 'https://www.snapdeal.com/product/quantron-jerry-qmu540-wired-mouse/644123372138',
            'phone.jpeg': 'https://www.snapdeal.com/search?keyword=phones+under+10000',
            'tab.jpeg': 'https://www.snapdeal.com/search?keyword=Samsung+Galaxy+Tab+A9'
        }
    
    def get_url(self, filename, product_name):
        """Get Snapdeal URL for product"""
        urls = self.get_product_urls()
        
        if filename.lower() in urls:
            return urls[filename.lower()]
        else:
            # Create search URL
            search_term = product_name.replace(' ', '%20')
            return f"{self.base_url}/search?keyword={search_term}"
    
    def get_price_from_database(self, filename, database):
        """Extract Snapdeal price from database"""
        for line in database:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 6 and parts[0].lower() == filename.lower():
                    return parts[5]  # Snapdeal price is 6th column
        return "Check Price"