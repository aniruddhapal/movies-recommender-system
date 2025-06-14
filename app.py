# app.py
import streamlit as st
import pickle
import pandas as pd
import requests
import time

# --- Use a Session object for persistent connections ---
session = requests.Session()

# --- The Caching Decorator ---
# This is the key to solving the problem. Streamlit will store the result
# of this function. If it's called again with the same movie_id, it will
# return the stored result instantly without running the function or hitting the API.
# The cache is cleared when the app is restarted.
@st.cache_data
def fetch_poster(movie_id):
    """
    Fetches the movie poster from The Movie Database (TMDB) API with retry logic.
    This function is cached to avoid repeated API calls for the same movie.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2f488a95dfb2437a9d3fb1933cf19074&language=en-US"
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                print(f"SUCCESS: Fetched poster for movie_id {movie_id}")
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return None
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"API request failed for movie_id {movie_id} (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
            else:
                print(f"All retries failed for movie_id {movie_id}.")
                return None
    return None

# The caching for this function is even more important. It caches the entire
# list of recommended names and posters for a given movie title.
@st.cache_data
def recommend(movie):
    """
    Recommends 5 similar movies. The entire recommendation list is cached.
    """
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            # This will now use the cached version of fetch_poster if available
            recommended_movies_posters.append(fetch_poster(movie_id))
            
        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the dataset. Please select another one.")
        return [], []

# --- Load Artifacts ---
try:
    movies_dict = pickle.load(open('artifacts/movies_list.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model artifacts not found. Please run `create_artifacts.py` first.")
    st.stop()

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title('🎬 Content-Based Movie Recommender')
st.markdown("Select a movie to get five similar recommendations!")

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Recommend', key='recommend_button'):
    # When the button is clicked, we call the cached recommend function
    names, posters = recommend(selected_movie_name)
    
    if names:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                if posters[i]:
                    st.image(posters[i])
                else:
                    st.warning("Poster not available")
    else:
        st.warning("Could not find recommendations.")