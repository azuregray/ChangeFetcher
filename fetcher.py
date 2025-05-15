import requests
import hashlib
import os
import time
from bs4 import BeautifulSoup

# --- Configuration ---
WEBSITE_URL = "https://cetonline.karnataka.gov.in/kea/pgcet2025"  # Replace with the actual URL
CACHE_FILE = "website_cache.txt"

def fetch_website_content(url):
    """Fetches the content of a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        print('RECEIVED RESPONSE :: ', response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website: {e}")
        return None

def calculate_hash(content):
    """Calculates the MD5 hash of the given content."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def load_cached_hash():
    """Loads the previously stored hash from the cache file."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return f.readline().strip()
    return None

def save_cached_hash(hash_value):
    """Saves the current hash to the cache file."""
    with open(CACHE_FILE, "w") as f:
        f.write(hash_value)

def check_for_updates():
    """Fetches the website, checks for changes, and prints a message."""
    print(f"Checking {WEBSITE_URL} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    current_content = fetch_website_content(WEBSITE_URL)
    if current_content:
        current_hash = calculate_hash(current_content)
        cached_hash = load_cached_hash()

        if cached_hash is not None and current_hash != cached_hash:
            print("***** WEBSITE CONTENT HAS CHANGED! *****")
            save_cached_hash(current_hash)
        elif cached_hash is None:
            print("Saving initial website content hash.")
            save_cached_hash(current_hash)
        else:
            print("No changes detected since the last check.")
    else:
        print("Could not fetch website content. Please check the URL and your internet connection.")

if __name__ == "__main__":
    check_for_updates()
    input("Press Enter to close the script.")