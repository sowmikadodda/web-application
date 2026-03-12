class FlipkartHandler:
    def __init__(self):
        self.base_url = "https://www.flipkart.com"
        
    def get_product_urls(self):
        """Flipkart product URLs mapping"""
        return {
          
            'charger.jpeg': 'https://www.flipkart.com/portronics-12-w-2-4-wall-charger-mobile-detachable-cable/p/itm23b662efb4410?pid=ACCFWFUZRVVAEGSG&lid=LSTACCFWFUZRVVAEGSGRP0KNV&marketplace=FLIPKART&q=charger%20under%20150&sattr[]=color&sattr[]=detachable_usb_cable&st=color',
            'fan.jpeg': 'https://www.flipkart.com/gestor-aero-deco-ultra-high-speed-48-inch-semi-decorative-36-months-warranty-anti-dust-1200-mm-ceiling-fan/p/itmebfbd86476508?pid=FANH99TQQJZRMGN9&lid=LSTFANH99TQQJZRMGN9OSZLOA&marketplace=FLIPKART&q=fans+under+1000&store=j9e%2Fabm%2Flbz&srno=s_1_3&otracker=search&otracker1=search&fm=organic&iid=1027bceb-e5bb-4f9c-81a2-951dee6d8811.FANH99TQQJZRMGN9.SEARCH&ppt=pp&ppn=pp&ssid=4gcwlx8kyo0000001765902822183&qH=519d4a700ff83560',
            'gamepad.jpeg': 'https://www.flipkart.com/hicle-silicone-protective-cover-ps5-controller-anti-slip-dotted-grip-sleeve-case-gamepad/p/itm5411c2122c98a?pid=ACCHDTEHGF55DXDK&lid=LSTACCHDTEHGF55DXDKJBL2UQ&marketplace=FLIPKART&q=gamepad+under+500&store=4rr%2Fkm5%2Fr39%2Fa7g&srno=s_1_22&otracker=search&otracker1=search&fm=organic&iid=en_3qb5UajYa0xgy75jA8U0OgYPxbH-CNoZsFUmtDHVdnvBw1qNH32NOYjwG3K46CE0PUHKlpm9p-elYlOT6qQj5A%3D%3D&ppt=pp&ppn=pp&ssid=nmlkj93odc0000001765950498050&qH=9e795817216eb224',
            'keyboard.jpeg': 'https://www.flipkart.com/zebronics-zeb-km-2100-wired-usb-standard-desktop-keyboard-compatible-desktop-laptop-mac-stand-support-multimedia-keys-km-2100/p/itme4d7408f2405e?pid=ACCEZ3YWU75CERHH&lid=LSTACCEZ3YWU75CERHHOG2UIJ&marketplace=FLIPKART&q=computer+keyboards+under+200&store=6bo%2Ftia%2F8pp%2Fwap&spotlightTagId=default_BestsellerId_6bo%2Ftia%2F8pp%2Fwap&srno=s_1_5&otracker=search&otracker1=search&fm=Search&iid=a0b99c12-20d2-4d27-b84d-ecfa38979785.ACCEZ3YWU75CERHH.SEARCH&ppt=sp&ppn=sp&ssid=qc0z6vcm7k0000001765948359722&qH=f7083e42beb4d462',
            'kettle.jpeg': 'https://www.flipkart.com/havok-electric-kettle-stainless-steel-body/p/itm2e3626b13330e?pid=EKTHBZZTKUGBFJPZ&lid=LSTEKTHBZZTKUGBFJPZ1XSP3B&marketplace=FLIPKART&q=kettle+under+500&store=j9e%2Fm38%2Fxrv&srno=s_1_7&otracker=search&otracker1=search&fm=organic&iid=dd0e527b-7db1-4ddd-9c12-ec8a353f980f.EKTHBZZTKUGBFJPZ.SEARCH&ppt=pp&ppn=pp&ssid=h5c9sy676o0000001765973490151&qH=7e444831eed0a985',
            'laptop.jpeg': 'https://www.flipkart.com/lenovo-100e-chromebook-gen-4-mediatek-kompanio-520-4-gb-32-gb-emmc-storage-chrome-os-82w00004ha/p/itm1ae5f82096ad9?pid=COMHA9FK8YXVUUWA&lid=LSTCOMHA9FK8YXVUUWAAREQMZ&marketplace=FLIPKART&q=laptop&store=6bo%2Fb5g&srno=s_1_3&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_ps&fm=organic&iid=b12b3c1d-74bf-4707-93b7-cd7d7a4e8ee0.COMHA9FK8YXVUUWA.SEARCH&ppt=hp&ppn=homepage&ssid=k9l4j0sa3k0000001765962734260&qH=312f91285e048e09',
            'mouse.jpeg': 'https://www.flipkart.com/flipkart-smartbuy-os807-wired-ambidextrous-optical-mouse/p/itm35eb15977dff4?pid=ACCGFGTQ3NS3BYMK&lid=LSTACCGFGTQ3NS3BYMK97ORMR&marketplace=FLIPKART&q=mouse+under+100&store=6bo%2Ftia%2F8pp%2Fp0w&srno=s_1_1&otracker=AS_QueryStore_OrganicAutoSuggest_1_11_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_11_na_na_na&fm=search-autosuggest&iid=0cfb217e-418f-44a1-81af-51623f38764e.ACCGFGTQ3NS3BYMK.SEARCH&ppt=sp&ppn=sp&ssid=pvduvlu9z40000001765948786172&qH=b2d0083d5ae12110',
            'phone.jpeg': 'https://www.flipkart.com/ai-pulse-blue-64-gb/p/itm131a44071789c?pid=MOBHDDQXW4ZVQFFX&lid=LSTMOBHDDQXW4ZVQFFXZCFXAD&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_7&otracker=CLP_Filters&fm=organic&iid=f19db39d-7c55-43f7-8784-a25cf5d0f2f6.MOBHDDQXW4ZVQFFX.SEARCH&ppt=clp&ppn=mobile-phones-store&ssid=eecczbqdlc0000001766039899801',
            'tab.jpeg': 'https://www.flipkart.com/kall-n1-1-gb-8-gb-1-gb-ram-8-rom-inch-4g-tablet-gold/p/itmd833162700ba6?pid=TABEUGKYJ7NM3CFV&lid=LSTTABEUGKYJ7NM3CFVF5K2CM&marketplace=FLIPKART&q=tab+under+10000&store=tyy%2Fhry&spotlightTagId=default_TrendingId_tyy%2Fhry&srno=s_1_16&otracker=search&otracker1=search&fm=Search&iid=19799a17-b349-4306-b158-2254dd167beb.TABEUGKYJ7NM3CFV.SEARCH&ppt=sp&ppn=sp&ssid=n6i648ml4g0000001765949569461&qH=c254eb5b9778d744',
            'earbuds.jpeg': 'https://www.flipkart.com/techio-black-earbuds-true-wireless-stereo-noise-cancelling-bluetooth/p/itm0276b3ead64b1?pid=ACCHB7E3HF9YTZZC&lid=LSTACCHB7E3HF9YTZZC45UZCN&marketplace=FLIPKART&q=lowest+earbuds&store=0pm%2Ffcn%2F821&spotlightTagId=default_BestsellerId_0pm%2Ffcn%2F821&srno=s_1_15&otracker=search&otracker1=search&fm=Search&iid=19f97688-4a22-4c60-ae9b-8370a359138d.ACCHB7E3HF9YTZZC.SEARCH&ppt=sp&ppn=sp&ssid=0mbkyyjghc0000001766073567226&qH=46f5f7b4fdc2555e'
        }

    def get_url(self, filename, product_name):
        """Get Flipkart URL for product"""
        urls = self.get_product_urls()
        if filename.lower() in urls:
            return urls[filename.lower()]
        else:
            search_term = product_name.replace(' ', '%20')
            return f"{self.base_url}/search?q={search_term}"

    def get_price_from_database(self, filename, database):
        """Extract Flipkart price from database"""
        for line in database:
            if line.strip():
                parts = line.strip().split('|')
                if len(parts) == 6 and parts[0].lower() == filename.lower():
                    return parts[4]  # Flipkart price is 5th column
        return "Check Price"
