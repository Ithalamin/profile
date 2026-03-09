import requests
from bs4 import BeautifulSoup
import re

# --- CONFIGURATION (শুধু এখানে আপনার ID দিন) ---
AFFILIATE_TAG = "yourid-21" 
CATEGORY_URL = "https://www.amazon.in/gp/movers-and-shakers/electronics/" # যে ক্যাটাগরি চান

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def hunt_deals():
    r = requests.get(CATEGORY_URL, headers=HEADERS)
    soup = BeautifulSoup(r.content, "html.parser")
    products = []
    
    # Amazon-এর প্রোডাক্ট কার্ডগুলো খুঁজে বের করা
    cards = soup.select('.p13n-grid-content')[:12] # টপ ১২টি প্রোডাক্ট
    
    for card in cards:
        try:
            title = card.find('div', class_='_cDEAy_p13n-sc-css-line-clamp-3_33mR2').text.strip()
            link_path = card.find('a', class_='a-link-normal')['href']
            # Clean URL and inject tag
            clean_url = "https://www.amazon.in" + link_path.split('?')[0] + f"?tag={AFFILIATE_TAG}"
            img = card.find('img')['src']
            price = card.find('span', class_='_cDEAy_price_33mR2').text.strip()
            
            products.append({"title": title[:50], "link": clean_url, "img": img, "price": price})
        except: continue
    return products

def inject_to_html(products):
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

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
