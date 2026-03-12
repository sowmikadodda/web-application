class AmazonHandler:
    def __init__(self):
        self.base_url = "https://www.amazon.in"
        
    def get_product_urls(self):
        """Amazon product URLs mapping"""
        return {
            'earbuds.jpeg': 'https://www.amazon.in/ENTERPRISE-Bluetooth-Headphones-Microphone-Connection/dp/B0G1YFB141/ref=sr_1_5?crid=1IRHREKXAEMXX&dib=eyJ2IjoiMSJ9.qGiptwXMnMDrDnxoCUBuoH3oCiE4ExFlitYqkeKrRvlYGwGIy9RI8h3028QDT5JVzcWn6AULrkObfpYDNUsifnEvV5sOpzdlGMviAPC2RDfwiMe78b69UcoCWtPDWJtgpZdaanWPREPc4UlmHc_D2r1MSbcxgA_r8y69cwBClEr_qM4o1tCj_sT09ejCbXwvceJbH6KVeZU8qqHoHfc20cg8Am2fq3OkVTL0MY7gmco.3gSsW9rHUwY9tynfSs5DKNdQmSLxrjlHyu3ernMdfuQ&dib_tag=se&keywords=bluetooth%2Bunder%2B500&qid=1765988827&sprefix=bluetooth%2Bunder%2B500%2Caps%2C238&sr=8-5&th=1',
            'charger.jpeg': 'https://www.amazon.in/Portronics-Adapto-12-Charger-Samsung/dp/B0CHJQ28F3/ref=sr_1_10?crid=2SIHFVCHZ5YT4&dib=eyJ2IjoiMSJ9.6rxqzP33EVX_7DnUqc4Rl0HfyhWxVviGBp9lJUm1GGCRvWUWvtsTUWrf2LJba1SWblpLo2Qefryyl02gnXY4ceGAIAAy8aRPRFid7j5RIqn4ffWPjJ3FhTTJrCudc7AckqJYac7dTWKYf7-eqv6jZe7q6aufkKVScuMfuL3FPxUwl8KVOLqmUxDfSYcNddoMBlPJR32OugKuHsRDO6YWQiYiyfL4O4AAaDcoJlFIANk.fcwIEgd22D8E3c6POfvCkgve-XIIoe4-ZaJrueuaHMg&dib_tag=se&keywords=charger&qid=1765964741&sprefix=charger%2Caps%2C209&sr=8-10',
            'fan.jpeg': 'https://www.amazon.in/Crompton-SUREBREEZE-HILLBRIZ-Ceiling-efficient/dp/B0BTS6RG52',
            'gamepad.jpeg': 'https://www.amazon.in/Enter-USB-Game-Vibration-GPV/dp/B00E9891EK',
            'keyboard.jpeg': 'https://www.amazon.in/Frontech-Jil1672-Usb-Keyboard-Black/dp/B013WC1D62/ref=dp_prsubs_d_sccl_1/522-6196843-1463537?pd_rd_w=vknKo&content-id=amzn1.sym.d0178f36-5905-465c-827f-0b2e79e77036&pf_rd_p=d0178f36-5905-465c-827f-0b2e79e77036&pf_rd_r=CJARPKPEXAX8XJ5C9AG2&pd_rd_wg=WI8U2&pd_rd_r=d00b5374-239d-4b38-b8c1-a38b716bbe47&pd_rd_i=B013WC1D62&psc',
            'kettle.jpeg': 'https://www.amazon.in/NeuOn-Electric-Kettle-Stainless-Steel/dp/B0DTHJJ3FR/ref=sr_1_5?crid=1FP6TOQ6I6CYP&dib=eyJ2IjoiMSJ9.sYmxfBaA0Su5GkGUgD4otFtSrCRuVOL7GD3FWd8miPFaRIHsLqeB0_vt7-q-qL6Of9GdOC8Bsk3HqLA1mb9YUcDHFR0OenwDdThNmiLcI3jX5B4cFvPC8Y8S41FK4rPUOsFGeaU3i17RnEp-UTmKNOliQjLtsu6sgMZmRqYiA_04pbPKAZgPdepd4NxaYM0CMZmZqxnzwNuW6l7E0KjEaEqlnnhVGglPUqKvO_af9YQ.ovxGdnG1EGX7RZFrHqcERwaWfkSWBW-dQUEVD9bXcS0&dib_tag=se&keywords=kettle+under+400&qid=1765973371&s=kitchen&sprefix=kettle+under+400%2Ckitchen%2C173&sr=1-5',
            'laptop.jpeg': 'https://www.amazon.in/Neopticon-BrowseBook-Student-Celeron-Windows/dp/B0FC64RYH1/?_encoding=UTF8&pd_rd_w=eGfoR&content-id=amzn1.sym.47226dd1-3657-494d-8578-f5621c2124b3&pf_rd_p=47226dd1-3657-494d-8578-f5621c2124b3&pf_rd_r=11HK2WX7J2W5KCS1X5FP&pd_rd_wg=gywX6&pd_rd_r=4d3a174a-206d-4bea-a957-7b2198f17b98&ref_=pd_hp_d_atf_dealz_cs&th=1',
            'mouse.jpeg': 'https://www.amazon.in/ZEBRONICS-Zeb-Comfort-3-Button-Optical-Windows/dp/B079Y6JZC8',
            'phone.jpeg': 'https://www.amazon.in/Lava-Bold-N1-Fingerprint-Phone-Case/dp/B0F83HMDDR/ref=sr_1_3?crid=PXH0AJVTWVXR&dib=eyJ2IjoiMSJ9.OHUZ-P_amRFhrPNaplBBDqqq2L8w95PAm8npJfi0TVZ_7e9gjVAdp8LP4sAKxd5dYt-E7KBDvv8bBO8fi-8dQAWhlydR5Hog18SOtKoYgMt_DANFmEmoDenf27otRViOTznq361D6c6l5PMTgAZGvuz2Z_V0owbvGOXEyX1frD5PyAPP83jvg4lknnblHNug.A4V6aqJfeyaq5b7CHBvia2WGXCmMh1tKWxNRp56gb9s&dib_tag=se&keywords=phones%2Bunder%2B10000&psr=EY17&qid=1765974132&s=todays-deals&sprefix=phones%2Bunder%2B10000%2Ctodays-deals%2C220&sr=1-3&th=1',
            'tab.jpeg': 'https://www.amazon.in/Samsung-Galaxy-Tab-A9-Expandable/dp/B0CJ37223B'
        }
    
    def get_url(self, filename, product_name):
        """Get Amazon URL for product"""
        urls = self.get_product_urls()
        
        if filename.lower() in urls:
            return urls[filename.lower()]
        else:
            # Create search URL
            search_term = product_name.replace(' ', '+')
            return f"{self.base_url}/s?k={search_term}&exact=true"
    
    def get_price_from_database(self, filename, database):
        """Extract Amazon price from database"""
        for line in database:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 6 and parts[0].lower() == filename.lower():
                    return parts[3]  # Amazon price is 4th column
        return "Check Price"