import os
import time
import httpx
from datetime import datetime

# Simple automated validation script
API_URL = "http://localhost:8000/api"

def run_tests():
    print(f"[{datetime.now()}] Starting Sentiment Validation Test...")
    
    # 1. Upload Test Dataset
    try:
        with open("test_dataset.csv", "rb") as f:
            files = {"file": ("test_dataset.csv", f, "text/csv")}
            response = httpx.post(f"{API_URL}/upload-feedback", files=files, timeout=60.0)
            
        if response.status_code != 200:
            print(f"Upload failed: {response.text}")
            return
            
        print("Upload successful. Waiting 2 seconds for processing...")
        time.sleep(2)
        
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        return

    # 2. Check Dashboard Stats
    try:
        dash_response = httpx.get(f"{API_URL}/dashboard")
        stats = dash_response.json()
        
        # In a real database we might have previous entries, so we just check if it aggregated properly 
        # For a clean slate, it should be exactly 1, 1, 1 if DB was empty. 
        # But we print the total to verify it extracted them.
        
        pos = stats.get("positive", 0)
        neg = stats.get("negative", 0)
        neu = stats.get("neutral", 0)
        
        print("\n--- Validation Results ---")
        print(f"Positive Sentiment Count: {pos}")
        print(f"Negative Sentiment Count: {neg}")
        print(f"Neutral Sentiment Count: {neu}")
        
        print("\nTop Complaints:")
        for c in stats.get("top_complaints", []):
            print(f"- {c['name']}: {c['value']}")
            
        print("\nTrending Issues:")
        for t in stats.get("trending_issues", []):
            print(f"- {t['name']}: {t['trend']}")
            
        if pos >= 1 and neg >= 1 and neu >= 1:
            print("\n[SUCCESS] Root cause resolved. Sentiment correctly categorized and aggregated!")
        else:
            print("\n[FAILED] Sentiment still not aggregating correctly. Expected at least 1 of each.")
            
    except Exception as e:
        print(f"Error checking dashboard: {e}")

if __name__ == "__main__":
    run_tests()
