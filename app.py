# app.py
import streamlit as st
import pickle
import pandas as pd
import requests
import os

# --- No more data processing imports like CountVectorizer or nltk ---

session = requests.Session()

# The @st.cache_data decorator is still very important for the API calls
@st.cache_data
def fetch_poster(movie_id):
    """
    Fetches the movie poster from The Movie Database (TMDB) API.
    """
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?2f488a95dfb2437a9d3fb1933cf19074&language=en-US"
        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except requests.exceptions.RequestException as e:
        print(f"API request failed for movie_id {movie_id}: {e}")
    return None

def recommend(movie):
    """
    Recommends 5 similar movies based on the pre-computed similarity matrix.
    """
    try:
        # Find the index of the movie that was selected
        movie_index = movies[movies['title'] == movie].index[0]
        
        # Get the similarity scores for that movie with all other movies
        distances = similarity[movie_index]
        
        # Sort the movies based on the similarity scores and get the top 5
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(movie_id))
            
        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []

# --- Load Pre-Computed Artifacts ---
print("Loading pre-computed artifacts...")
try:
    # We load the dataframe of movies
    movies_dict = pickle.load(open('artifacts/movies_list.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    # We load the final similarity matrix
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model artifacts not found. This might happen on the first deploy. The app should auto-restart shortly.")
    st.stop()
print("Artifacts loaded successfully.")

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title('🎬 Content-Based Movie Recommender')
st.markdown("Select a movie to get five similar recommendations!")

selected_movie_name = st.selectbox(
    'Which movie have you enjoyed?',
    movies['title'].values
)

if st.button('Recommend'):
    with st.spinner('Finding recommendations for you...'):
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