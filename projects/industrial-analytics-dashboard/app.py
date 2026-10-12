"""Interactive synthetic factory production dashboard."""
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Industrial Analytics Studio", layout="wide")
st.title("Industrial Analytics Studio")
st.caption("Synthetic factory operations data for demonstration — not actual company data.")

@st.cache_data
def load_data(days=90):
    rng = np.random.default_rng(42)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)
    throughput = np.maximum(0, rng.normal(990, 125, days)).round()
    rejects = rng.binomial(throughput.astype(int), 0.025)
    downtime = rng.gamma(2.0, 13.0, days)
    return pd.DataFrame({"date": dates, "units": throughput, "rejected": rejects, "downtime_min": downtime})

df = load_data()
line = st.selectbox("Metric", ["units", "rejected", "downtime_min"])
c1, c2, c3 = st.columns(3)
c1.metric("Total units", f"{int(df.units.sum()):,}")
c2.metric("Reject rate", f"{100 * df.rejected.sum() / df.units.sum():.2f}%")
c3.metric("Total downtime (hours)", f"{df.downtime_min.sum() / 60:.1f}")
st.subheader("Daily trend")
st.line_chart(df.set_index("date")[[line]])
st.subheader("Recent data")
st.dataframe(df.tail(14), use_container_width=True)
st.download_button("Download generated sample CSV", df.to_csv(index=False), "sample_operations.csv", "text/csv")
