import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Netflix Pricing Dashboard", layout="centered")

st.title("🎬 Netflix Pricing Strategy Dashboard")
st.write("""
This dashboard simulates the impact of different pricing strategies on Netflix's subscriber and revenue growth between 2025 and 2029.
""")

# Define pricing scenarios
pricing_scenarios = {
    "Aggressive (Low Price)": {"price": 7.99, "growth_rate": 0.10},
    "Balanced (Current Price)": {"price": 17.99, "growth_rate": 0.06},
    "Premium (High Price)": {"price": 24.99, "growth_rate": 0.03}
}

years = list(range(2025, 2030))
initial_subs = 1_000_000

forecast_df = pd.DataFrame({"Year": years})

# Simulate data
for strategy, details in pricing_scenarios.items():
    subs = [initial_subs]
    revenue = [initial_subs * details["price"]]
    for _ in range(1, len(years)):
        new_subs = subs[-1] * (1 + details["growth_rate"])
        subs.append(new_subs)
        revenue.append(new_subs * details["price"])
    forecast_df[strategy + " Subs"] = subs
    forecast_df[strategy + " Revenue"] = revenue

# Let user pick a strategy
selected_strategy = st.selectbox("Choose a strategy to explore:", list(pricing_scenarios.keys()))

# Plot revenue forecast
st.subheader("📈 Revenue Forecast")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(forecast_df["Year"], forecast_df[selected_strategy + " Revenue"], marker='o', color='dodgerblue')
ax.set_title(f"Revenue Growth: {selected_strategy}")
ax.set_xlabel("Year")
ax.set_ylabel("Total Revenue (USD)")
ax.grid(True)
st.pyplot(fig)

# Plot subscriber forecast
st.subheader("👥 Subscriber Forecast")
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(forecast_df["Year"], forecast_df[selected_strategy + " Subs"], marker='s', color='seagreen')
ax2.set_title(f"Subscriber Growth: {selected_strategy}")
ax2.set_xlabel("Year")
ax2.set_ylabel("Total Subscribers")
ax2.grid(True)
st.pyplot(fig2)

# Show table
st.subheader("📊 Forecast Data")
st.dataframe(forecast_df)
