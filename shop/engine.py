import requests
from bs4 import BeautifulSoup
import os

# --- ELITE CONFIGURATION ---
AFFILIATE_TAG = "yourid-21"  # Replace with your actual Amazon ID
AMAZON_DEALS_URL = "https://www.amazon.in/gp/movers-and-shakers/electronics/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def get_deals():
    try:
        r = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.content, "html.parser")
        items = []
        
        cards = soup.select('.p13n-grid-content')[:12]
        for card in cards:
            title = card.find('div', class_='_cDEAy_p13n-sc-css-line-clamp-3_33mR2').text.strip()[:45] + "..."
            raw_link = card.find('a', class_='a-link-normal')['href']
            # Injecting Affiliate Tag surgically
            clean_link = "https://www.amazon.in" + raw_link.split('?')[0] + f"?tag={AFFILIATE_TAG}"
            img = card.find('img')['src']
            price = card.find('span', class_='_cDEAy_price_33mR2').text.strip()
            items.append({"title": title, "link": clean_link, "img": img, "price": price})
        return items
    except Exception as e:
        print(f"Scrape Error: {e}")
        return []

def update_html(products):
    # Locate index.html in the same 'shop' directory
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, "index.html")
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for i, p in enumerate(products, 1):
        if soup.find(id=f"p{i}-title"):
            soup.find(id=f"p{i}-title").string = p['title']
            soup.find(id=f"p{i}-price").string = p['price']
            soup.find(id=f"p{i}-img")['src'] = p['img']
            soup.find(id=f"p{i}-link")['href'] = p['link']

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    print("Initiating Stealth Hunter...")
    data = get_deals()
    if data:
        update_html(data)
        print(f"System Optimized: {len(data)} Deals Injected with tag {AFFILIATE_TAG}")
    for i, p in enumerate(products, 1):
        if soup.find(id=f"p{i}-title"):
            soup.find(id=f"p{i}-title").string = p['title']
            soup.find(id=f"p{i}-price").string = p['price']
            soup.find(id=f"p{i}-img")['src'] = p['img']
            soup.find(id=f"p{i}-link")['href'] = p['link']

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    print("🕵️ Starting Stealth Hunter...")
    found_products = hunt_deals()
    if found_products:
        inject_to_html(found_products)
        print(f"🔥 Successfully injected {len(found_products)} deals with tag: {AFFILIATE_TAG}")
