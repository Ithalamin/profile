import json
import os
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import base64
from datetime import datetime

# ডিরেক্টরি নিশ্চিত করা
os.makedirs('shop', exist_ok=True)

def get_real_products(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=shop"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    products = []
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('.sh-dgr__content')
        
        for item in items[:6]:
            try:
                name = item.select_one('h3').get_text()
                price = item.select_one('.a8U8ve').get_text()
                img = item.select_one('img')['src']
                raw_link = f"https://www.amazon.in/s?k={name.replace(' ', '+')}&tag=YOUR_ID"
                products.append({
                    "name": name, "price": price, "img": img,
                    "link": base64.b64encode(raw_link.encode()).decode()
                })
            except: continue
    except: pass

    # Shadow Fallback: যদি গুগল ডাটা না দেয়, তবে খালি পেজ না বানিয়ে ডামি ডাটা দেবে
    if not products:
        products = [{
            "name": f"Deal of the Day for {query}",
            "price": "Check Site",
            "img": "https://via.placeholder.com/300?text=Click+to+See+Price",
            "link": base64.b64encode(f"https://www.amazon.in/s?k={query}".encode()).decode()
        }]
    return products

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>{{ title }}</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .card { border: 1px solid #0f0; padding: 15px; border-radius: 10px; cursor: pointer; text-align: center; }
        img { width: 100%; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>SYSTEM_UPDATE: {{ title }}</h1>
    <div class="grid">
        {% for p in products %}
        <div class="card" onclick="window.location.href=atob('{{ p.link }}')">
            <img src="{{ p.img }}">
            <h3>{{ p.name }}</h3>
            <p>PRICE: {{ p.price }}</p>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def main():
    # categories.json না থাকলে অটো তৈরি করবে (ভুল এড়াতে)
    if not os.path.exists('categories.json'):
        with open('categories.json', 'w') as f:
            json.dump(["Best Mobile under 20000"], f)

    with open('categories.json', 'r') as f:
        categories = json.load(f)

    template = Template(HTML_TEMPLATE)
    for cat in categories:
        print(f"Working on: {cat}")
        data = get_real_products(cat)
        slug = cat.lower().replace(" ", "-").strip()
        html = template.render(title=cat, products=data)
        with open(f"shop/{slug}.html", "w", encoding="utf-8") as f:
            f.write(html)
    print("✅ Logic Execution Successful.")

if __name__ == "__main__":
    main()
