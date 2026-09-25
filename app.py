import os
import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# TinyFish Automation Endpoint
TINYFISH_AGENT_URL = "https://agent.tinyfish.ai/v1/automation/run"
TINYFISH_API_KEY = os.environ.get("TINYFISH_API_KEY", "your_free_tinyfish_key_here")

# Public mock online store optimized for e-commerce parsing
TARGET_STORE = "https://scrapeme.live"

def search_clothing_with_agent(query):
    headers = {
        "X-API-Key": TINYFISH_API_KEY,
        "Content-Type": "application/json"
    }
    
    # We instruct the TinyFish web agent with a structured execution goal
    payload = {
        "url": TARGET_STORE,
        "goal": f"Find clothing items matching '{query}'. Extract their exact titles, prices, and absolute image source URLs. Return them structured exactly as a JSON array named 'products' containing fields: title, price, image."
    }
    
    try:
        response = requests.post(TINYFISH_AGENT_URL, json=payload, headers=headers)
        if response.status_code == 200:
            agent_data = response.json()
            # The structured JSON parsed from the live site session
            return agent_data.get("result", {}).get("products", [])
    except Exception as e:
        print(f"Agent error: {e}")
        
    # Instant offline fallback data if your API key isn't loaded yet
    return [
        {"title": f"Custom {query.capitalize()} Basic", "price": "£19.99", "image": "https://unsplash.com"},
        {"title": f"Premium {query.capitalize()} Outerwear", "price": "£54.00", "image": "https://unsplash.com"}
    ]

# Layout template built with Tailwind UI components
STORE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TinyFish Agent Store</title>
    <script src="https://jsdelivr.net"></script>
</head>
<body class="bg-slate-50 text-slate-800">
    <nav class="bg-white border-b border-slate-200">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-blue-600">🌊 TinyFish Agentic Retail</h1>
            <span class="text-xs bg-blue-100 text-blue-800 px-2.5 py-1 rounded-full font-medium">Agent Automation Active</span>
        </div>
    </nav>

    <main class="max-w-6xl mx-auto px-4 py-10">
        <!-- Search Controller Bar -->
        <div class="max-w-xl mb-12">
            <h2 class="text-3xl font-extrabold tracking-tight mb-2">On-Demand Sourcing</h2>
            <p class="text-slate-500 mb-4">Enter a clothing style. The backend AI Agent will crawl the web to find matches instantly.</p>
            <form action="/" method="GET" class="flex gap-2">
                <input type="text" name="q" placeholder="e.g., Hoodie, Pants, Jacket..." value="{{ current_query }}" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-blue-500 bg-white">
                <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-lg transition">Sourcing Scan</button>
            </form>
        </div>

        <!-- Dynamic Results Layout -->
        <div>
            <h3 class="text-lg font-bold text-slate-900 mb-6">Showing results for: <span class="text-blue-600">"{{ current_query }}"</span></h3>
            
            {% if products %}
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {% for product in products %}
                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xs hover:shadow-md transition duration-200 flex flex-col">
                    <div class="aspect-square bg-slate-100 relative overflow-hidden">
                        <img src="{{ product.image }}" alt="{{ product.title }}" class="w-full h-full object-cover">
                    </div>
                    <div class="p-4 flex flex-col flex-grow">
                        <h4 class="font-semibold text-slate-900 line-clamp-2 mb-1">{{ product.title }}</h4>
                        <p class="text-sm font-medium text-blue-600 mb-4">{{ product.price }}</p>
                        <button class="mt-auto w-full bg-slate-900 hover:bg-slate-800 text-white text-sm font-medium py-2 rounded-lg transition">Add to Cart</button>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <p class="text-slate-500">No items found. Try another fashion search phrase!</p>
            {% endif %}
        </div>
    </main>
</body>
</html>
"""

@app.route('/')
def index():
    # Grab search parameter or default to "shirt"
    search_query = request.args.get('q', 'shirt')
    discovered_products = search_clothing_with_agent(search_query)
    return render_template_string(STORE_TEMPLATE, products=discovered_products, current_query=search_query)

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
