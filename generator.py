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
        items = soup.select('.sh-dgr__content, .i0X6df')
        
        for item in items[:8]:
            try:
                name = item.select_one('h3').text
                price = item.select_one('.a8U8ve, .OFF33c').text
                img = item.select_one('img')['src']
                link = base64.b64encode(f"https://www.amazon.in/s?k={name.replace(' ', '+')}&tag=YOUR_ID".encode()).decode()
                products.append({"name": name, "price": price, "img": img, "link": link})
            except: continue
    except: pass
    
    if not products:
        products = [{"name": f"Latest {query} Model", "price": "Check Offer", "img": "https://via.placeholder.com/200x200?text=Product+Image", "link": base64.b64encode(f"https://www.amazon.in/s?k={query}".encode()).decode()}]
    return products

# --- Templates ---
PRODUCT_TEMPLATE = """
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
        .product-card { background: #fff; border-bottom: 1px solid #f0f0f0; display: flex; padding: 15px; text-decoration: none; color: inherit; transition: 0.2s; cursor: pointer; align-items: center; }
        .img-box { width: 30%; min-width: 100px; text-align: center; }
        .img-box img { max-width: 100%; max-height: 150px; object-fit: contain; }
        .details { width: 70%; padding-left: 20px; }
        .details h3 { font-size: 18px; margin: 0; color: #212121; font-weight: 500; }
        .price { font-size: 22px; font-weight: bold; color: #388e3c; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="header">{{ title }}</div>
    <div class="container">
        {% for p in products %}
        <div class="product-card" onclick="window.location.href=atob('{{ p.link }}')">
            <div class="img-box"><img src="{{ p.img }}"></div>
            <div class="details"><h3>{{ p.name }}</h3><div class="price">{{ p.price }}</div></div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elite Affiliate Store</title>
    <style>
        body { background: #f1f3f6; font-family: Roboto, sans-serif; margin: 0; padding: 0; }
        .nav { background: #2874f0; color: white; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; }
        .category-list { max-width: 600px; margin: 20px auto; padding: 0 10px; }
        .cat-item { background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; display: block; text-decoration: none; color: #212121; font-weight: 500; border-left: 5px solid #2874f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .cat-item:hover { background: #e0e0e0; }
    </style>
</head>
<body>
    <div class="nav">Explore Categories</div>
    <div class="category-list">
        {% for cat in categories %}
        <a href="{{ cat.slug }}.html" class="cat-item">{{ cat.name }} ></a>
        {% endfor %}
    </div>
</body>
</html>
"""

def build():
    with open('categories.json', 'r') as f:
        categories = json.load(f)
    
    today = datetime.now().strftime("%Y-%m-%d")
    prod_temp = Template(PRODUCT_TEMPLATE)
    
    cat_data_for_index = []

    for cat in categories:
        print(f"Shadowing: {cat}")
        data = fetch_data(cat)
        slug = cat.lower().replace(" ", "-").strip()
        cat_data_for_index.append({"name": cat, "slug": slug})
        
        with open(f"shop/{slug}.html", "w", encoding="utf-8") as f:
            f.write(prod_temp.render(title=cat, products=data, date=today))
    
    # Master Index তৈরি করা
    print("Generating Master Index...")
    index_temp = Template(INDEX_TEMPLATE)
    with open("shop/index.html", "w", encoding="utf-8") as f:
        f.write(index_temp.render(categories=cat_data_for_index))
    
    print("🎯 Execution Complete. Master Page Live.")

if __name__ == "__main__":
    build()
