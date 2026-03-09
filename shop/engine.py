import requests
from bs4 import BeautifulSoup
import os
import time

# --- ELITE CONFIGURATION ---
AFFILIATE_TAG = "yourid-21"  # Replace with your actual Amazon ID
AMAZON_DEALS_URL = "https://www.amazon.in/gp/movers-and-shakers/electronics/"

# Advanced Stealth Headers to bypass Amazon's bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

def get_deals():
    items = []
    try:
        # Adding a small delay to mimic human behavior
        time.sleep(2)
        r = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=30)
        
        if r.status_code != 200:
            print(f"Access Denied: Status Code {r.status_code}")
            return []

        soup = BeautifulSoup(r.content, "html.parser")
        
        # New selector for Amazon Movers & Shakers
        cards = soup.find_all('div', {'id': 'gridItemRoot'})[:12]
        
        if not cards:
            print("System Alert: No product cards found. Amazon might be blocking the request.")
            return []

        for card in cards:
            try:
                # Surgical extraction using broad selectors
                title_el = card.find('div', class_='_cDEAy_p13n-sc-css-line-clamp-3_33mR2')
                link_el = card.find('a', class_='a-link-normal')
                img_el = card.find('img')
                price_el = card.find('span', class_='_cDEAy_price_33mR2')

                if all([title_el, link_el, img_el, price_el]):
                    title = title_el.text.strip()[:45] + "..."
                    raw_link = link_path = link_el['href']
                    clean_link = "https://www.amazon.in" + raw_link.split('?')[0] + f"?tag={AFFILIATE_TAG}"
                    img = img_el['src']
                    price = price_el.text.strip()
                    
                    items.append({"title": title, "link": clean_link, "img": img, "price": price})
            except Exception as inner_e:
                continue
                
        return items
    except Exception as e:
        print(f"Critical System Error: {e}")
        return []

def update_html(products):
    if not products:
        print("Update Aborted: No data to inject.")
        return

    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "index.html")
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found!")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for i, p in enumerate(products, 1):
        target_title = soup.find(id=f"p{i}-title")
        if target_title:
            target_title.string = p['title']
            soup.find(id=f"p{i}-price").string = p['price']
            soup.find(id=f"p{i}-img")['src'] = p['img']
            soup.find(id=f"p{i}-link")['href'] = p['link']
            print(f"Injected: Product {i}")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    print("🕵️ Initiating Stealth Hunter...")
    data = get_deals()
    if data:
        update_html(data)
        print(f"🔥 Successfully injected {len(data)} deals.")
    else:
        print("❌ Scrape failed. Check logs.")
