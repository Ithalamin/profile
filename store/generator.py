import json
import base64
import requests
from bs4 import BeautifulSoup
from jinja2 import Template

# Stealth Template with Dynamic SEO
MASTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ category }} - Elite Picks</title>
    <style>
        body { background: #050505; color: #eee; font-family: sans-serif; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { border: 1px solid #333; padding: 15px; border-radius: 12px; transition: 0.3s; cursor: pointer; }
        .card:hover { border-color: #00ff00; box-shadow: 0 0 15px #00ff0033; }
        img { width: 100%; border-radius: 8px; }
        .price { color: #00ff00; font-size: 1.5rem; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>Top {{ category }} (Updated Live)</h1>
    <div class="grid">
        {% for p in products %}
        <div class="card" onclick="visit('{{ p.link }}')">
            <img src="{{ p.image }}">
            <h3>{{ p.name }}</h3>
            <div class="price">{{ p.price }}</div>
            <p>Click for Direct Deal</p>
        </div>
        {% endfor %}
    </div>
    <script>
        function visit(enc) { window.location.href = atob(enc); }
    </script>
</body>
</html>
"""

def fetch_trending_products(query):
    # Shadow Hack: Google Shopping search URL formatting
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=shop"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    # Surgical extraction of Product Cards (CSS classes will vary, must be tuned)
    for item in soup.select('.sh-dgr__content')[:8]: # Top 8 products
        try:
            name = item.select_one('h3').text
            price = item.select_one('.a8U8ve').text
            link = "https://google.com" + item.select_one('a')['href']
            img = item.select_one('img')['src']
            
            products.append({
                "name": name,
                "price": price,
                "image": img,
                "link": base64.b64encode(link.encode()).decode()
            })
        except: continue
    return products

def build_empire():
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    
    template = Template(MASTER_TEMPLATE)
    
    for cat in categories:
        print(f"🕵️ Searching trends for: {cat}")
        products = fetch_trending_products(cat)
        
        if products:
            slug = cat.lower().replace(" ", "-")
            html = template.render(category=cat, products=products)
            with open(f"{slug}.html", "w", encoding="utf-8") as f:
                f.write(html)

if __name__ == "__main__":
    build_empire()
