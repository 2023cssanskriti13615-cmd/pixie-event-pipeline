import streamlit as st
import pandas as pd
from supabase import create_client
st.set_page_config(page_title="Pixie Event Insights", page_icon="📈")
st.title(" Real-Time Event Analytics")
url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_KEY"
supabase = create_client(url, key)
res = supabase.table("events").select("*").execute()
df = pd.DataFrame(res.data)
if not df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Events", len(df))
    col2.metric("Locations", df['location'].nunique())
    col3.metric("Latest Sync", "Just Now")
    st.write("### Events Distribution")
    location_counts = df['location'].value_counts()
    st.bar_chart(location_counts)
    st.write("### Scraped Event List")
    st.dataframe(df[['title', 'event_date', 'location']], use_container_width=True)
else:
    st.warning("No data found in Supabase. Run the scraper first!")