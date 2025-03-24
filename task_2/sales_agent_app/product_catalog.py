# Sample product database with detailed information
product_catalog = {
    "smartphone": [
        {"name": "iPhone 15 Pro", "price": 999, "brand": "Apple",
            "specs": "6.1-inch display, A17 chip"},
        {"name": "Samsung Galaxy S23 Ultra", "price": 1199,
            "brand": "Samsung", "specs": "6.8-inch display, Snapdragon 8 Gen 2"},
        {"name": "Google Pixel 8 Pro", "price": 899,
            "brand": "Google", "specs": "6.7-inch display, Tensor G3"},
        {"name": "OnePlus 11", "price": 699, "brand": "OnePlus",
            "specs": "6.7-inch display, Snapdragon 8 Gen 2"},
        {"name": "Xiaomi 13 Pro", "price": 799, "brand": "Xiaomi",
            "specs": "6.73-inch display, Snapdragon 8 Gen 2"}
    ],
    "laptop": [
        {"name": "MacBook Air M2", "price": 1199, "brand": "Apple",
            "specs": "13.6-inch display, M2 chip"},
        {"name": "Dell XPS 15", "price": 1499, "brand": "Dell",
            "specs": "15.6-inch display, Intel Core i7"},
        {"name": "HP Spectre x360", "price": 1299, "brand": "HP",
            "specs": "13.5-inch display, Intel Core i5"},
        {"name": "Lenovo ThinkPad X1", "price": 1599, "brand": "Lenovo",
            "specs": "14-inch display, Intel Core i7"},
        {"name": "Asus ROG Zephyrus G14", "price": 1399,
            "brand": "Asus", "specs": "14-inch display, AMD Ryzen 9"}
    ],

}

# Category aliases mapping
category_aliases = {
    "mobile": "smartphone",
    "mobile phone": "smartphone",
    "phone": "smartphone",
    "cell phone": "smartphone",
    "computers": "laptop",
    "notebook": "laptop",

}

# Function to get product recommendations


def get_recommendation(category, budget=None):
    # Check if category is an alias
    if category.lower() in category_aliases:
        category = category_aliases[category.lower()]

    products = product_catalog.get(category.lower(), [])
    if budget:
        products = [
            product for product in products if product["price"] <= budget]
    return products

# Function to detect product category in user input...


def detect_categories(user_input):
    detected_categories = []
    user_input_lower = user_input.lower()

    # Check direct categories
    for category in product_catalog.keys():
        if category.lower() in user_input_lower:
            detected_categories.append(category)

    # Check aliases
    for alias, category in category_aliases.items():
        if alias.lower() in user_input_lower and category not in detected_categories:
            detected_categories.append(category)

    return detected_categories
