"""
Generates a realistic synthetic retail superstore dataset (~1000 rows).
Run: python generate_data.py  -> creates sample_sales.csv in this folder.

I wrote this because real sales datasets either need credentials or are way
too big. This gives me something I can actually demo and mess around with.
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

REGIONS = {
    "East": ["New York", "Florida", "Pennsylvania", "Georgia", "Virginia"],
    "West": ["California", "Washington", "Oregon", "Arizona", "Nevada"],
    "Central": ["Texas", "Illinois", "Ohio", "Missouri", "Colorado"],
    "South": ["North Carolina", "Tennessee", "Alabama", "Louisiana", "Kentucky"],
}

PRODUCTS = {
    "Furniture": {
        "Chairs": ["Ergonomic Office Chair", "Wooden Dining Chair", "Mesh Task Chair"],
        "Tables": ["Oak Coffee Table", "Standing Desk", "Folding Conference Table"],
        "Bookcases": ["5-Shelf Bookcase", "Corner Bookshelf", "Wall-Mount Shelf"],
        "Furnishings": ["Floor Lamp", "Area Rug 5x7", "Wall Clock"],
    },
    "Office Supplies": {
        "Binders": ["Leather Binder Set", "3-Ring Binder Pack"],
        "Paper": ["A4 Copy Paper 500ct", "Recycled Notebook Pack"],
        "Art": ["Acrylic Paint Set", "Sketchbook A3"],
        "Storage": ["File Organizer Box", "Desk Drawer Unit"],
        "Appliances": ["Paper Shredder", "Label Printer"],
    },
    "Technology": {
        "Phones": ["Wireless Headset", "Smartphone Stand"],
        "Accessories": ["USB-C Hub", "Wireless Mouse", "Laptop Sleeve"],
        "Machines": ["Laser Printer", "Portable Scanner"],
        "Copiers": ["Office Copier Pro", "Compact Copier"],
    },
}

SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]


def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def main():
    start = datetime(2023, 1, 1)
    end = datetime(2024, 12, 31)

    rows = []
    order_id = 1000
    for _ in range(1000):
        order_date = random_date(start, end)
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        region = random.choice(list(REGIONS.keys()))
        state = random.choice(REGIONS[region])
        category = random.choice(list(PRODUCTS.keys()))
        sub_cat = random.choice(list(PRODUCTS[category].keys()))
        product = random.choice(PRODUCTS[category][sub_cat])

        # make some categories pricier on purpose, keeps the analysis interesting
        base = {"Furniture": 280, "Technology": 220, "Office Supplies": 45}[category]
        qty = random.randint(1, 6)
        discount = random.choice([0, 0, 0, 0.1, 0.15, 0.2, 0.3])
        sales = round(base * qty * random.uniform(0.7, 1.4) * (1 - discount), 2)
        # furniture with big discounts tends to lose money, which is realistic lol
        margin = random.uniform(0.05, 0.35) - (discount * 0.8)
        profit = round(sales * margin, 2)

        rows.append({
            "Order ID": f"ORD-{order_id}",
            "Order Date": order_date.strftime("%Y-%m-%d"),
            "Ship Date": ship_date.strftime("%Y-%m-%d"),
            "Ship Mode": random.choice(SHIP_MODES),
            "Customer Segment": random.choice(SEGMENTS),
            "Region": region,
            "State": state,
            "Category": category,
            "Sub-Category": sub_cat,
            "Product Name": product,
            "Quantity": qty,
            "Discount": discount,
            "Sales": sales,
            "Profit": profit,
        })
        order_id += 1

    with open("sample_sales.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to sample_sales.csv")


if __name__ == "__main__":
    main()
