"""
Retail Sales Insights Dashboard

Run: streamlit run app.py

Main dashboard for the project. Sidebar filters, KPI cards, charts,
and an automated insights panel that writes a plain-English summary of
what the numbers are saying. The insights generator is template-based
on purpose - no API key needed to demo it. There's a commented example
at the bottom of generate_insights() showing how to swap in the OpenAI
API if you want real LLM output later.
"""
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Retail Sales Insights", layout="wide")

# ---------------- data ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_sales.csv", parse_dates=["Order Date"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Margin %"] = (df["Profit"] / df["Sales"] * 100).round(1)
    return df

df = load_data()

# ---------------- insights generator ----------------
def generate_insights(data: pd.DataFrame) -> str:
    """Turns the key metrics into a natural-language executive summary.

    Template-based so it works offline. Swap the return with the OpenAI
    snippet below if you want actual LLM-generated text.
    """
    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    margin = total_profit / total_sales * 100 if total_sales else 0
    orders = len(data)

    top_cat = data.groupby("Category")["Sales"].sum().idxmax()
    top_region = data.groupby("Region")["Profit"].sum().idxmax()
    worst_region = data.groupby("Region")["Profit"].sum().idxmin()

    monthly = data.groupby("Month")["Sales"].sum()
    trend = "upward" if len(monthly) > 1 and monthly.iloc[-1] > monthly.iloc[0] else "flat or declining"

    # discount story - this was the most interesting finding in my EDA
    # (same bucket as analysis.py and the SQL: strictly above 20%)
    heavy_disc = data[data["Discount"] > 0.2]
    heavy_margin = (heavy_disc["Profit"] / heavy_disc["Sales"]).mean() * 100 if len(heavy_disc) else 0

    lines = [
        f"Over the selected period, the business generated ${total_sales:,.0f} in sales "
        f"across {orders:,} orders, with ${total_profit:,.0f} in profit ({margin:.1f}% margin).",
        f"{top_cat} is the top revenue driver, while {top_region} delivered the highest profit. "
        f"{worst_region} is lagging on profit and may need a closer look at pricing or product mix.",
        f"Sales momentum looks {trend} across the period.",
    ]
    if heavy_margin < 0:
        lines.append(
            f"One red flag: orders with discounts above 20% are losing money "
            f"({heavy_margin:.1f}% margin). I'd recommend capping deep discounts or "
            f"restricting them to high-margin categories."
        )
    lines.append(
        "Suggested next steps: protect margin in the strongest region, review the "
        "discount policy, and double down on the top-performing category."
    )
    return " ".join(lines)

    # --- to use a real LLM instead, uncomment this and pip install openai ---
    # from openai import OpenAI
    # client = OpenAI()  # needs OPENAI_API_KEY in your environment
    # summary_stats = data.groupby("Category").agg(
    #     sales=("Sales", "sum"), profit=("Profit", "sum")).to_string()
    # resp = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system",
    #          "content": "You are a senior data analyst. Write a concise executive "
    #                     "summary of these retail sales metrics with 2-3 actionable "
    #                     "recommendations."},
    #         {"role": "user", "content": summary_stats},
    #     ],
    # )
    # return resp.choices[0].message.content


# ---------------- sidebar filters ----------------
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()),
                                 default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()),
                                    default=sorted(df["Category"].unique()))
segments = st.sidebar.multiselect("Customer Segment", sorted(df["Customer Segment"].unique()),
                                  default=sorted(df["Customer Segment"].unique()))

filtered = df[df["Region"].isin(regions) &
              df["Category"].isin(categories) &
              df["Customer Segment"].isin(segments)]

# ---------------- header ----------------
st.title("Retail Sales Insights Dashboard")
st.caption("Interactive sales performance + automated executive summary")

if filtered.empty:
    st.warning("No data matches those filters - try widening them a bit.")
    st.stop()

# ---------------- KPI cards ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${filtered['Sales'].sum():,.0f}")
c2.metric("Total Profit", f"${filtered['Profit'].sum():,.0f}")
margin = filtered["Profit"].sum() / filtered["Sales"].sum() * 100
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("Orders", f"{len(filtered):,}")

# ---------------- charts ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Category")
    cat_sales = filtered.groupby("Category")["Sales"].sum().reset_index()
    st.plotly_chart(px.bar(cat_sales, x="Category", y="Sales",
                           color="Category", text_auto=".2s"), use_container_width=True)

with col2:
    st.subheader("Profit by Region")
    reg_profit = filtered.groupby("Region")["Profit"].sum().reset_index()
    st.plotly_chart(px.bar(reg_profit, x="Region", y="Profit",
                           color="Region", text_auto=".2s"), use_container_width=True)

st.subheader("Monthly Sales Trend")
monthly = filtered.groupby("Month")["Sales"].sum().reset_index()
st.plotly_chart(px.line(monthly, x="Month", y="Sales", markers=True),
                use_container_width=True)

st.subheader("Top 10 Products by Profit")
top_prod = filtered.groupby("Product Name")["Profit"].sum().nlargest(10).reset_index()
st.plotly_chart(px.bar(top_prod, x="Profit", y="Product Name", orientation="h",
                       text_auto=".2s"), use_container_width=True)

# ---------------- insights ----------------
st.subheader("Automated Insights")
if st.button("Generate summary"):
    with st.spinner("Crunching the numbers..."):
        st.info(generate_insights(filtered))
else:
    st.caption("Click to generate a plain-English summary of the filtered data.")

# raw data peek, because someone always asks for it
with st.expander("View raw data"):
    st.dataframe(filtered.head(50))
