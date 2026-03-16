import json
import os
import base64
from jinja2 import Template
from datetime import datetime

# স্যাম্পল প্রোডাক্ট ডাটা (পরবর্তীতে এটি স্ক্র্যাপার দিয়ে রিপ্লেস করা যাবে)
def get_mock_products(category):
    return [
        {"name": f"Premium {category} 1", "price": "19,999", "img": "https://via.placeholder.com/300", "link": "https://amazon.com"},
        {"name": f"Elite {category} 2", "price": "14,500", "img": "https://via.placeholder.com/300", "link": "https://flipkart.com"}
    ]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        body { background: #111; color: white; font-family: sans-serif; text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; padding: 20px; }
        .card { border: 1px solid #333; padding: 15px; border-radius: 10px; cursor: pointer; }
        .card:hover { border-color: #00ff00; }
        img { width: 100%; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="grid">
        {% for p in products %}
        <div class="card" onclick="location.href='{{ p.link }}'">
            <img src="{{ p.img }}">
            <h3>{{ p.name }}</h3>
            <p style="color:#00ff00">Price: ₹{{ p.price }}</p>
        </div>
        {% endfor %}
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
