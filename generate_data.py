import pandas as pd
import numpy as np
import duckdb
from datetime import datetime, timedelta
import os

np.random.seed(42)

os.makedirs("data", exist_ok=True)

customers = []
subscriptions = []

regions = ["Ireland", "UK", "Germany", "France", "Spain"]
segments = ["SMB", "Mid-Market", "Enterprise"]
plans = ["Basic", "Professional", "Enterprise"]

for customer_id in range(1, 5001):
    region = np.random.choice(regions)
    segment = np.random.choice(segments, p=[0.6, 0.3, 0.1])
    signup_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 700))

    customers.append({
        "customer_id": customer_id,
        "region": region,
        "segment": segment,
        "signup_date": signup_date.date()
    })

    monthly_revenue = np.random.choice([49, 99, 199, 499, 999])
    churned = np.random.choice([0, 1], p=[0.82, 0.18])

    subscriptions.append({
        "subscription_id": customer_id,
        "customer_id": customer_id,
        "plan": np.random.choice(plans),
        "monthly_revenue": monthly_revenue,
        "is_churned": churned,
        "created_at": signup_date.date()
    })

customers_df = pd.DataFrame(customers)
subscriptions_df = pd.DataFrame(subscriptions)

customers_df.to_csv("data/customers.csv", index=False)
subscriptions_df.to_csv("data/subscriptions.csv", index=False)

con = duckdb.connect("data/saas_analytics.duckdb")

con.execute("DROP TABLE IF EXISTS raw_customers")
con.execute("DROP TABLE IF EXISTS raw_subscriptions")

con.execute("CREATE TABLE raw_customers AS SELECT * FROM customers_df")
con.execute("CREATE TABLE raw_subscriptions AS SELECT * FROM subscriptions_df")

con.close()

print("Data generated successfully.")
print("Created 5,000 customers and subscription records.")