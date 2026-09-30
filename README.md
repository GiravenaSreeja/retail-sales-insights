# Retail Sales Insights Dashboard

An end-to-end data analytics project: I took a retail sales dataset, ran a full exploratory analysis in Python, answered the same questions in SQL, and built an interactive Streamlit dashboard on top — with an automated insights generator that writes a plain-English executive summary of whatever the filters show.

## Why I built this

I wanted a project that looks like actual analyst work, not a Kaggle notebook that ends at a confusion matrix. So I picked the most classic analyst task there is — "here's two years of sales data, tell us what's going on" — and did the whole thing: cleaning, EDA, SQL, dashboard, and a stakeholder-facing summary.

The summary feature came from a real frustration: dashboards are great, but managers still ask "so what does this mean?" The insights generator closes that gap by turning the filtered metrics into a short written summary with recommendations. It runs on templates so it works with zero setup, but I left a commented example showing how to plug in the OpenAI API for real LLM output.

## What's in here

- **data/sample_sales.csv** — 1,000 rows of synthetic retail data (orders, regions, categories, discounts, profit). Generated with `data/generate_data.py` so it's reproducible.
- **analysis.py** — the EDA: category/region performance, monthly trends, and the discount-vs-margin analysis. Saves plots to `images/`.
- **app.py** — the Streamlit dashboard: sidebar filters, KPI cards, Plotly charts, and the auto-summary button.
- **sql/analysis_queries.sql** — 8 queries covering KPIs, trends, discount buckets, loss-making orders, and segment analysis.
- **images/** — charts from the EDA.

## Key findings

The most interesting thing I found: **orders with discounts of 20% or more have negative average margin (-4.4%)**. The company is literally paying customers to take products at those discount levels. That's the kind of finding that actually changes a promo strategy, and it's the first thing the summary flags.

Other takeaways:
- Technology has the highest margin (12.8%), Furniture drives the most revenue
- South region leads on profit; East lags despite decent sales
- Consumer is the biggest segment by both orders and revenue

## How to run it

```bash
pip install -r requirements.txt

# run the EDA
python analysis.py

# launch the dashboard
streamlit run app.py
```

The SQL file is standalone — load the CSV into any MySQL/Postgres table called `sales` and run the queries. (Note: `DATE_FORMAT` is MySQL syntax; swap for `TO_CHAR` in Postgres.)

## What I learned

- Honestly, the hardest part was making the synthetic data behave realistically. My first version had profit totally uncorrelated with discount, which made the whole analysis boring. Adding the "deep discounts kill margin" relationship made it feel like a real business problem.
- Plotly + Streamlit is a great combo for demos, but caching (`@st.cache_data`) matters — the dashboard was noticeably laggy before I added it.
- Writing the template-based summary taught me a lot about prompt structure. Even without an LLM, you have to decide *which* numbers matter and *what story* they tell, which is the actual analyst skill. Swapping in a real LLM later is mostly a formatting problem once the logic is right.

## Future improvements

- [ ] Wire up the OpenAI API option for truly dynamic summaries
- [ ] Add a forecast tab (prophet or even simple moving average)
- [ ] Let users upload their own CSV instead of the sample data
- [ ] Add customer-level RFM segmentation

## Tech stack

Python, Pandas, Matplotlib, Streamlit, Plotly, SQL (MySQL)
