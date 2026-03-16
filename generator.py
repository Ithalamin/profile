import json
import os
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import base64

# এই ফাংশনটি এখন গুগল থেকে আসল ডাটা আনবে
def get_real_products(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=shop"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # গুগল শপিং থেকে টপ ৫টি প্রোডাক্ট স্ক্র্যাপ করা
        for item in soup.select('.sh-dgr__content')[:5]:
            name = item.select_one('h3').text
            price = item.select_one('.a8U8ve').text
            # আপনার অ্যাফিলিয়েট আইডি এখানে যোগ হবে
            raw_link = "https://www.amazon.in/s?k=" + name.replace(' ', '+') + "&tag=YOUR_AFF_ID_HERE"
            img = item.select_one('img')['src']
            
            products.append({
                "name": name,
                "price": price,
                "img": img,
                "link": base64.b64encode(raw_link.encode()).decode() # লিঙ্ক হাইড করা
            })
        return products
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

# আপনার মেইন ইঞ্জিন
def build_empire():
    if not os.path.exists('shop'): os.makedirs('shop')
    
    with open('categories.json', 'r') as f:
        categories = json.load(f)

    # আপনার ডিজাইন টেমপ্লেট (আগেরটাই থাকছে)
    with open('shop/template.html', 'r') as t_file: # টেমপ্লেট আলাদা ফাইলে রাখলে সুবিধা
        template = Template(t_file.read())

    for cat in categories:
        print(f"🕵️ Harvesting: {cat}")
        real_data = get_real_products(cat)
        
        if real_data:
            slug = cat.lower().replace(" ", "-")
            output = template.render(title=cat, products=real_data)
            with open(f"shop/{slug}.html", "w", encoding="utf-8") as f:
                f.write(output)

if __name__ == "__main__":
    build_empire()        {% endfor %}
    </div>
</body>
</html>
"""

def build_shop():
    # নিশ্চিত করা যে shop ফোল্ডারটি আছে
    if not os.path.exists('shop'):
        os.makedirs('shop')

    with open('categories.json', 'r') as f:
        categories = json.load(f)

    template = Template(HTML_TEMPLATE)

    for cat in categories:
        slug = cat.lower().replace(" ", "-")
        products = get_mock_products(cat) # এখানে স্ক্র্যাপার বসবে
        
        output = template.render(title=cat, products=products)
        
        # ফাইলটি shop/ ফোল্ডারে সেভ হবে
        with open(f"shop/{slug}.html", "w", encoding="utf-8") as f:
            f.write(output)

    print(f"✅ {len(categories)} Pages Created/Updated in /shop directory")

if __name__ == "__main__":
    build_shop()
