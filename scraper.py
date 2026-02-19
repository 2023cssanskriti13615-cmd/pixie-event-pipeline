import requests
from bs4 import BeautifulSoup
import hashlib

def run_real_scraper():
    # Using a stable events page for testing
    url = "https://www.eventbrite.com/d/online/events/" 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('h3') 
    
    if not titles:
        print("❌ Scraper found 0 titles. The website might be blocking us or the tags changed.")
        return []

    events_to_upload = []
    
    for item in titles:
        name = item.get_text().strip()
        # Create a unique ID
        unique_id = hashlib.md5(name.encode()).hexdigest()
        
        event_obj = {
            "id": unique_id,
            "title": name,
            "event_date": "2026-03-01", # Placeholder for now
            "location": "Online"
        }
        
        # --- THE PUSH TO SUPABASE ---
        try:
            supabase.table("events").upsert(event_obj).execute()
            events_to_upload.append(event_obj)
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")

    return events_to_upload

# RUN IT
results = run_real_scraper()
print(f"Success! Found and uploaded {len(results)} events.")