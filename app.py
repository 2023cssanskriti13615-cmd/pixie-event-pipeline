import streamlit as st
import pandas as pd
from supabase import create_client

# Page Config
st.set_page_config(page_title="Pixie Event Insights", page_icon="📈")
st.title("🚀 Real-Time Event Analytics")

# --- THE FIX IS HERE ---
# We tell Streamlit to grab the keys from the "Advanced Settings" box
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

# Now we connect using the REAL keys
supabase = create_client(url, key)
# -----------------------

res = supabase.table("events").select("*").execute()
df = pd.DataFrame(res.data)

if not df.empty:
    st.metric("Total Events Scraped", len(df))
    st.write("### Event List")
    st.dataframe(df[['title', 'event_date', 'location']])
else:
    st.warning("No data found in the database.")
