import json
import os
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import base64
from datetime import datetime

# ১. পাথ এবং ডিরেক্টরি চেক
if not os.path.exists('shop'):
    os.makedirs('shop')

def get_real_products(query):
    # Shadow Scraper: Bypassing standard bot detection
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=shop"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # গুগল শপিং ডাটা এক্সট্রাকশন
        items = soup.select('.sh-dgr__content')
        for item in items[:6]: # প্রতি পেজে ৬টি করে প্রোডাক্ট
            try:
                name = item.select_one('h3').get_text()
                price = item.select_one('.a8U8ve').get_text()
                img = item.select_one('img')['src']
                # এফিলিয়েট লিঙ্ক প্রোটেকশন
                raw_link = f"https://www.amazon.in/s?k={name.replace(' ', '+')}&tag=YOUR_ID"
                
                products.append({
                    "name": name,
                    "price": price,
                    "img": img,
                    "link": base64.b64encode(raw_link.encode()).decode()
                })
            except Exception: continue
        return products
    except Exception as e:
        print(f"Scraper Error for {query}: {e}")
        return []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { background: #0a0a0a; color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1200px; margin: auto; }
        .card { background: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 15px; text-align: center; transition: 0.3s; cursor: pointer; }
        .card:hover { border-color: #00ff00; transform: translateY(-5px); }
        img { width: 100%; height: 200px; object-fit: contain; border-radius: 10px; }
        h1 { text-align: center; color: #00ff00; }
        .price { font-size: 1.5rem; color: #00ff00; margin: 10px 0; }
        .btn { background: #00ff00; color: #000; padding: 10px; border-radius: 5px; font-weight: bold; text-decoration: none; display: block; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <p style="text-align:center">Last Sync: {{ date }}</p>
    <div class="grid">
        {% for p in products %}
        <div class="card" onclick="window.location.href=atob('{{ p.link }}')">
            <img src="{{ p.img }}" alt="{{ p.name }}">
            <h3>{{ p.name }}</h3>
            <div class="price">{{ p.price }}</div>
            <div class="btn">Check Underground Deal</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def main():
    if not os.path.exists('categories.json'):
        print("Error: categories.json missing")
        return

    with open('categories.json', 'r') as f:
        categories = json.load(f)

    template = Template(HTML_TEMPLATE)
    today = datetime.now().strftime("%Y-%m-%d")

    for cat in categories:
        print(f"📡 Syncing: {cat}")
        data = get_real_products(cat)
        if data:
            slug = cat.lower().replace(" ", "-").strip()
            html = template.render(title=cat, products=data, date=today)
            with open(f"shop/{slug}.html", "w", encoding="utf-8") as f:
                f.write(html)
    
    print("✅ All systems operational.")

if __name__ == "__main__":
    main()
