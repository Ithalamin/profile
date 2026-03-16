import json, os, requests, base64
from bs4 import BeautifulSoup
from jinja2 import Template
from datetime import datetime

os.makedirs('shop', exist_ok=True)

def fetch_data(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}+price+india&tbm=shop"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    products = []
    try:
        r = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        # এই অংশটি গুগলের লেটেস্ট শপিং গ্রিড ডিটেক্ট করবে
        items = soup.select('.sh-dgr__content, .i0X6df')
        
        for item in items[:8]:
            try:
                name = item.select_one('h3').text
                price = item.select_one('.a8U8ve, .OFF33c').text
                img = item.select_one('img')['src']
                # সরাসরি আমাজন সার্চ লিঙ্ক (অ্যাফিলিয়েট ট্যাগসহ)
                link = base64.b64encode(f"https://www.amazon.in/s?k={name.replace(' ', '+')}&tag=YOUR_ID".encode()).decode()
                products.append({"name": name, "price": price, "img": img, "link": link})
            except: continue
    except: pass
    
    # যদি ডাটা না পায় তবে সুন্দর ডামি ডাটা (যাতে পেজ খালি না থাকে)
    if not products:
        products = [{"name": f"Latest {query} Model", "price": "Check Offer", "img": "https://via.placeholder.com/200x200?text=Product+Image", "link": base64.b64encode(f"https://www.amazon.in/s?k={query}".encode()).decode()}]
    return products

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { background: #f1f3f6; color: #212121; font-family: Roboto, Arial, sans-serif; margin: 0; padding: 10px; }
        .header { background: #2874f0; color: white; padding: 15px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 10px; border-radius: 4px; }
        .container { max-width: 800px; margin: auto; }
        .product-card { 
            background: #fff; border-bottom: 1px solid #f0f0f0; 
            display: flex; padding: 15px; text-decoration: none; color: inherit;
            transition: 0.2s; cursor: pointer; align-items: center;
        }
        .product-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .img-box { width: 30%; min-width: 100px; text-align: center; }
        .img-box img { max-width: 100%; max-height: 150px; object-fit: contain; }
        .details { width: 70%; padding-left: 20px; }
        .details h3 { font-size: 18px; margin: 0 0 10px 0; color: #212121; font-weight: 500; }
        .price { font-size: 22px; font-weight: bold; color: #388e3c; margin-bottom: 10px; }
        .tagline { background: #388e3c; color: white; font-size: 12px; padding: 2px 6px; border-radius: 2px; display: inline-block; }
    </style>
</head>
<body>
    <div class="header">Elite Deals: {{ title }}</div>
    <div class="container">
        {% for p in products %}
        <div class="product-card" onclick="window.location.href=atob('{{ p.link }}')">
            <div class="img-box"><img src="{{ p.img }}" alt="product"></div>
            <div class="details">
                <h3>{{ p.name }}</h3>
                <div class="tagline">Free Delivery</div>
                <div class="price">{{ p.price }}</div>
                <div style="color: #2874f0; font-weight: bold;">Shop Now ></div>
            </div>
        </div>
        {% endfor %}
    </div>
    <p style="text-align:center; color: #878787; font-size: 12px; margin-top: 20px;">Updated: {{ date }}</p>
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
    print("🎯 Flipkart UI Engine Complete.")

if __name__ == "__main__":
    build()
