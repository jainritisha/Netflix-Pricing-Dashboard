import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------- Task 1: Modify Dataset for Ad-Supported Tier ----------
st.title("Netflix Ad-Supported Tier Pricing Analysis")
st.header("Task 1: Data Preparation")

st.write("### Step 1: Add Ad-Supported Plan")
st.write("We introduced a new plan type — 'Basic with Ads' priced at $6.99.")

# Sample data
data = pd.read_csv("netflix_users.csv")  # This should be your cleaned dataset

# Add 'plan_type' column
conditions = [
    data['Subscription Type'].str.lower().str.contains("basic"),
    data['Subscription Type'].str.lower().str.contains("standard"),
    data['Subscription Type'].str.lower().str.contains("premium")
]
choices = ['Basic with Ads', 'Standard', 'Premium']
data['plan_type'] = np.select(conditions, choices, default='Basic with Ads')

st.dataframe(data.head())

# ---------- Task 2: Churn Sensitivity Analysis ----------
st.header("Task 2: Churn Sensitivity Analysis")

st.write("### Step 1: Model churn impact from pricing changes")
plan_types = ['Basic with Ads', 'Standard', 'Premium']
base_prices = {'Basic with Ads': 6.99, 'Standard': 15.49, 'Premium': 19.99}
churn_elasticity = {'Basic with Ads': -0.3, 'Standard': -0.25, 'Premium': -0.2}

price_range = np.arange(4.99, 24.99, 1)
subscriber_base = {'Basic with Ads': 1000000, 'Standard': 800000, 'Premium': 500000}

st.write("We used elasticity formulas to simulate churn effect across different price points.")

churn_df = pd.DataFrame()
for plan in plan_types:
    churn_rates = []
    retained_users = []
    for price in price_range:
        change = (price - base_prices[plan]) / base_prices[plan]
        churn_rate = churn_elasticity[plan] * change
        churn_rates.append(churn_rate)
        retained = subscriber_base[plan] * (1 + churn_rate)
        retained_users.append(retained)
    churn_df[plan] = retained_users

churn_df['Price'] = price_range
churn_df.set_index('Price', inplace=True)

# Plot churn sensitivity
st.write("### Step 2: Churn Elasticity Graphs")
st.write("Each line shows how retained users change with price adjustments.")
fig, ax = plt.subplots()
for plan in plan_types:
    ax.plot(churn_df.index, churn_df[plan], label=plan)
ax.set_title("Churn Sensitivity by Plan")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Estimated Subscribers")
ax.legend(loc='upper right')
ax.grid(True)
st.pyplot(fig)

# ---------- Task 3: Pricing Optimization with Solver ----------
st.header("Task 3: Optimize Pricing Mix")

st.write("### Step 1: Revenue Maximization")
prices = {'Basic with Ads': 6.99, 'Standard': 15.49, 'Premium': 19.99}
users = {'Basic with Ads': 1000000, 'Standard': 800000, 'Premium': 500000}
revenues = {plan: prices[plan] * users[plan] for plan in plan_types}

st.write("Estimated revenue per plan:")
st.write(revenues)

# Simulate optimized scenario
optimized_prices = {'Basic with Ads': 7.99, 'Standard': 16.99, 'Premium': 21.99}
opt_revenues = {plan: optimized_prices[plan] * users[plan] * (1 + churn_elasticity[plan] * ((optimized_prices[plan] - prices[plan]) / prices[plan])) for plan in plan_types}

st.write("Optimized pricing scenario:")
st.write(opt_revenues)

# Plot Comparison
fig2, ax2 = plt.subplots()
ax2.bar(revenues.keys(), revenues.values(), alpha=0.5, label='Current')
ax2.bar(opt_revenues.keys(), opt_revenues.values(), alpha=0.5, label='Optimized')
ax2.set_title("Revenue Optimization")
ax2.set_ylabel("Total Revenue")
ax2.legend()
st.pyplot(fig2)

# ---------- Task 4: Long-Term Subscriber Growth ----------
st.header("Task 4: Forecast Long-Term Subscriber Growth")

years = list(range(2025, 2030))
base_growth = {
    'Basic with Ads': [1000000 * (1.05)**i for i in range(5)],
    'Standard': [800000 * (1.03)**i for i in range(5)],
    'Premium': [500000 * (1.02)**i for i in range(5)],
}
opt_growth = {
    'Basic with Ads': [1000000 * (1.07)**i for i in range(5)],
    'Standard': [800000 * (1.04)**i for i in range(5)],
    'Premium': [500000 * (1.03)**i for i in range(5)],
}

st.write("### Step 1: Simulated Growth Over Time")
st.write("Comparing base and optimized subscriber growth trajectories")
fig3, ax3 = plt.subplots()
for plan in plan_types:
    ax3.plot(years, base_growth[plan], '--', label=f"{plan} - Base")
    ax3.plot(years, opt_growth[plan], '-', label=f"{plan} - Optimized")
ax3.set_title("Forecasted Subscriber Growth (2025–2029)")
ax3.set_xlabel("Year")
ax3.set_ylabel("Subscribers")
ax3.legend(loc='lower right')
ax3.grid(True)
st.pyplot(fig3)

# Revenue Forecast from Strategy Scenarios
st.write("### Step 2: Forecast under Strategy Scenarios")
scenarios = {
    "Aggressive (Low Price)": {"price": 7.99, "growth_rate": 0.10},
    "Balanced (Current Price)": {"price": 17.99, "growth_rate": 0.06},
    "Premium (High Price)": {"price": 24.99, "growth_rate": 0.03},
}

forecast_df = pd.DataFrame({"Year": years})
initial_subs = 1_000_000

for strategy, config in scenarios.items():
    subs = [initial_subs]
    rev = [initial_subs * config["price"]]
    for _ in range(1, len(years)):
        subs.append(subs[-1] * (1 + config["growth_rate"]))
        rev.append(subs[-1] * config["price"])
    forecast_df[strategy + " Subs"] = subs
    forecast_df[strategy + " Revenue"] = rev

fig4, ax4 = plt.subplots()
for strategy in scenarios:
    ax4.plot(forecast_df["Year"], forecast_df[strategy + " Revenue"], label=strategy)
ax4.set_title("Revenue Forecast under Pricing Strategies")
ax4.set_xlabel("Year")
ax4.set_ylabel("Total Revenue (USD)")
ax4.legend(loc='lower right')
ax4.grid(True)
st.pyplot(fig4)
