
import streamlit as st
import pandas as pd

st.markdown("""
<style>
.stApp {
    background-color: #0D0D1A;
    background-image:
        linear-gradient(rgba(120, 60, 180, 0.15) 1px, transparent 1px),
        linear-gradient(90deg, rgba(120, 60, 180, 0.15) 1px, transparent 1px);
    background-size: 40px 40px;
}
h1 { color: #FF8C5A !important; }
h2, h3 { color: #FF8C5A !important; }
p, li, .stMarkdown { color: #D4A0C0 !important; }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/layoffs.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

st.title("CareerGenIQ")
st.subheader("Job Market Intelligence Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Layoff Events", f"{len(df):,}")
col2.metric("Total Jobs Lost", f"{int(df['total_laid_off'].sum()):,}")

st.markdown("""
*Companies aren't just cutting jobs — they're stringing candidates along. Multiple interview rounds, weeks of silence, and offers that never come. The uncertainty feels random, but the data tells a different story. This dashboard tracks where layoffs are happening, who's behind them, and why — so you can make smarter moves.*
""")

st.markdown("---")

st.subheader("When Did It Get This Bad?")
st.markdown("""
*Layoffs were relatively quiet through 2020 and 2021. Then late 2022 hit — and the market hasn't fully recovered since. This chart shows the full picture from the start of the pandemic to today.*
""")
time_data = df.groupby(df['date'].dt.to_period('M'))['total_laid_off'].sum()
time_data.index = time_data.index.astype(str)
st.line_chart(time_data)

st.markdown("---")

st.subheader("Which Industries Are Hit the Hardest?")
st.markdown("""
*Retail leads with over 106,000 layoffs since 2020 — January 2026 alone saw 16,116 jobs lost, the highest single month in this entire dataset. Most people assume it's tech at the top but the numbers say otherwise. Use the dropdown to explore any industry and see how layoffs have shifted over time.*
""")
industry_data = df[df["industry"] != "Other"].groupby("industry")["total_laid_off"].sum().sort_values(ascending=False).head(10)
st.bar_chart(industry_data)

industries = sorted(df[df["industry"] != "Other"]["industry"].dropna().unique())
selected_industry = st.selectbox("Explore an industry over time", industries)
industry_time = df[df["industry"] == selected_industry].groupby(df["date"].dt.to_period('M'))["total_laid_off"].sum()
industry_time.index = industry_time.index.astype(str)
st.line_chart(industry_time)

st.markdown("---")

st.subheader("Who Cut the Most?")
st.markdown("""
*Amazon leads with 58,124 layoffs — but every one of them is categorized as Retail in this dataset, which is why Retail ranks first overall. The data reflects how companies are classified, not just what they do. Before targeting any of these companies, do your due diligence — check whether they're currently hiring and when their last layoff round was.*
""")
top_companies = df.groupby("company")["total_laid_off"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_companies)

st.markdown("---")

st.markdown("""
*The job market feels unpredictable — but the data shows patterns. Knowing where the layoffs are happening and who's behind them won't guarantee a job, but it's a smarter starting point than applying blindly.*
""")
st.caption("Data: Layoffs.fyi — compiled by Roger Lee. Dataset via Kaggle by Swapnil Tripathi. Covers March 11, 2020 to present.")
