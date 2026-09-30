"""
Exploratory data analysis on the retail sales dataset.

Run: python analysis.py
(plots get saved to the images/ folder)

Nothing fancy here - just the standard questions I'd ask as an analyst:
where is the money coming from, where is it leaking, and what's trending.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8-whitegrid")
os.makedirs("images", exist_ok=True)

df = pd.read_csv("data/sample_sales.csv", parse_dates=["Order Date", "Ship Date"])
print("shape:", df.shape)
print(df.head(3))
print("\nnulls:\n", df.isnull().sum())

# quick sanity check on the money columns
print("\n", df[["Sales", "Profit", "Discount"]].describe().round(2))

# ---- 1. sales + profit by category ----
cat = df.groupby("Category").agg(total_sales=("Sales", "sum"),
                                 total_profit=("Profit", "sum"),
                                 orders=("Order ID", "count")).round(2)
cat["margin_pct"] = (cat["total_profit"] / cat["total_sales"] * 100).round(1)
print("\nby category:\n", cat)

# ---- 2. region performance ----
reg = df.groupby("Region").agg(sales=("Sales", "sum"), profit=("Profit", "sum")).round(2)
print("\nby region:\n", reg)

# ---- 3. monthly trend ----
df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
monthly = df.groupby("Month").agg(sales=("Sales", "sum"), profit=("Profit", "sum"))
print("\nlast 6 months:\n", monthly.tail(6))

# ---- 4. discount vs profit - the interesting one ----
# grouping discounts into buckets to see the pattern clearly
df["discount_bucket"] = pd.cut(df["Discount"], bins=[-0.01, 0, 0.1, 0.2, 1],
                               labels=["0%", "0-10%", "10-20%", "20%+"])
disc = df.groupby("discount_bucket", observed=True).agg(
    avg_margin=("Profit", lambda x: (x / df.loc[x.index, "Sales"]).mean() * 100),
    orders=("Order ID", "count")).round(1)
print("\ndiscount buckets:\n", disc)

# ---- plots ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
cat["total_sales"].plot(kind="bar", ax=axes[0], color="#4C78A8")
axes[0].set_title("Total Sales by Category")
axes[0].set_ylabel("Sales ($)")
cat["total_profit"].plot(kind="bar", ax=axes[1], color="#72B66A")
axes[1].set_title("Total Profit by Category")
plt.tight_layout()
plt.savefig("images/category_sales_profit.png")
plt.close()

monthly["sales"].plot(figsize=(10, 4), color="#4C78A8", marker="o")
plt.title("Monthly Sales Trend")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig("images/monthly_trend.png")
plt.close()

# top 10 products by profit - honestly surprised some of these
top_products = df.groupby("Product Name")["Profit"].sum().sort_values(ascending=False).head(10)
top_products.plot(kind="barh", figsize=(9, 5), color="#F58518")
plt.title("Top 10 Products by Profit")
plt.tight_layout()
plt.savefig("images/top_products.png")
plt.close()

print("\nsaved 3 plots to images/. done.")
