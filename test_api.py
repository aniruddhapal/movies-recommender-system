# test_api.py
import requests

# Use a known, valid movie ID. Avatar's ID is 19995.
MOVIE_ID = 19995 

# --- CRITICAL ---
# Go to the TMDB website, copy your API key AGAIN, and paste it here.
# Make sure there are no extra spaces or characters.
API_KEY = "YOUR_API_KEY_HERE"

# Construct the full URL
url = f"https://api.themoviedb.org/3/movie/11036?api_key=2f488a95dfb2437a9d3fb1933cf19074&language=en-US"

print(f"Attempting to connect to URL: {url}\n")

try:
    # Make a single, simple request with a timeout
    response = requests.get(url, timeout=10)

    # Print the HTTP status code. 200 means success.
    print(f"HTTP Status Code: {response.status_code}")

    # Check if the request was successful
    response.raise_for_status()  # This will raise an error for 4xx or 5xx codes

    # If successful, print the data
    data = response.json()
    print("\n--- SUCCESS ---")
    print("Successfully fetched data:")
    print(f"Movie Title: {data.get('title')}")
    print(f"Poster Path: {data.get('poster_path')}")
    print("-----------------")

except requests.exceptions.RequestException as e:
    print("\n--- FAILED ---")
    print(f"An error occurred: {e}")
    print("----------------")