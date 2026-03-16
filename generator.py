import json, os, requests, base64
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime

# ডিরেক্টরি প্রোটেকশন
os.makedirs('shop', exist_ok=True)

def fetch_data(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=shop"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    products = []
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.select('.sh-dgr__content')[:6]:
            try:
                name = item.select_one('h3').text
                price = item.select_one('.a8U8ve').text
                img = item.select_one('img')['src']
                link = base64.b64encode(f"https://www.amazon.in/s?k={name.replace(' ', '+')}&tag=YOUR_ID".encode()).decode()
                products.append({"name": name, "price": price, "img": img, "link": link})
            except: continue
    except: pass
    
    # Fallback: ডাটা না পেলে ডামি কন্টেন্ট (SEO বাঁচানোর জন্য)
    if not products:
        products = [{"name": f"Top Deal: {query}", "price": "Check Latest", "img": "https://via.placeholder.com/300", "link": base64.b64encode(f"https://www.amazon.in/s?k={query}".encode()).decode()}]
    return products

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { background: #000; color: #0f0; font-family: 'Courier New', monospace; padding: 20px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }
        .card { border: 1px solid #0f0; padding: 15px; border-radius: 10px; text-align: center; cursor: pointer; transition: 0.3s; }
        .card:hover { background: #0f0; color: #000; }
        img { width: 100%; height: 180px; object-fit: contain; }
        .btn { border: 1px solid #0f0; padding: 10px; margin-top: 10px; display: block; font-weight: bold; }
    </style>
</head>
<body>
    <h1>[SYSTEM_READY] - {{ title }}</h1>
    <p>Last Sync: {{ date }}</p>
    <div class="grid">
        {% for p in products %}
        <div class="card" onclick="window.location.href=atob('{{ p.link }}')">
            <img src="{{ p.img }}">
            <h3>{{ p.name }}</h3>
            <div class="price">PRICE: {{ p.price }}</div>
            <div class="btn">ACCESS DEAL</div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

def build():
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    template = Template(TEMPLATE)
    
    for cat in categories:
        print(f"Shadowing: {cat}")
        data = fetch_data(cat)
        slug = cat.lower().replace(" ", "-").strip()
        with open(f"shop/{slug}.html", "w", encoding="utf-8") as f:
            f.write(template.render(title=cat, products=data, date=today))
    print("🎯 Execution Complete.")

if __name__ == "__main__":
    build()
