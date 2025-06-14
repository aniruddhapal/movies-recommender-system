# create_artifacts.py
import pandas as pd
import numpy as np # Import numpy
import ast
import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import nltk

# Create Artifacts Directory
ARTIFACTS_DIR = 'artifacts'
if not os.path.exists(ARTIFACTS_DIR):
    os.makedirs(ARTIFACTS_DIR)
    print(f"Created directory: {ARTIFACTS_DIR}")

print("Loading data...")
credits = pd.read_csv('data/tmdb_5000_credits.csv')
movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
movies_df = movies_df.merge(credits, on='title')

# --- Feature Selection & Preprocessing ---
movies = movies_df[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

# Helper functions (they remain the same)
def safe_literal_eval(obj):
    try: return ast.literal_eval(obj)
    except (ValueError, SyntaxError): return []

def convert_top_3(obj):
    L = []
    counter = 0
    for i in safe_literal_eval(obj):
        if counter != 3: L.append(i['name']); counter += 1
        else: break
    return L

def fetch_director(obj):
    L = []
    for i in safe_literal_eval(obj):
        if i['job'] == 'Director': L.append(i['name']); break
    return L

lemmatizer = WordNetLemmatizer()
def lemma(text):
    y = [];
    for i in text.split(): y.append(lemmatizer.lemmatize(i))
    return " ".join(y)

print("Preprocessing and Feature Engineering...")
movies['genres'] = movies['genres'].apply(convert_top_3)
movies['keywords'] = movies['keywords'].apply(convert_top_3)
movies['cast'] = movies['cast'].apply(convert_top_3)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
new_df = movies[['movie_id', 'title', 'tags']].copy()

# --- OPTIMIZATION 1: Reduce vocabulary size ---
print("Vectorizing text with reduced features...")
cv = CountVectorizer(max_features=4000, stop_words='english') # Reduced from 5000 to 4000
vectors = cv.fit_transform(new_df['tags']).toarray()

# --- OPTIMIZATION 2: Change data type to save memory ---
print("Calculating cosine similarity with float32...")
similarity = cosine_similarity(vectors).astype(np.float32) # Convert to float32

# --- Save Artifacts ---
print("Saving artifacts...")
# Check the new size
print(f"New similarity matrix size: {similarity.nbytes / (1024*1024):.2f} MB")
pickle.dump(new_df.to_dict(), open(os.path.join(ARTIFACTS_DIR, 'movies_list.pkl'), 'wb'))
pickle.dump(similarity, open(os.path.join(ARTIFACTS_DIR, 'similarity.pkl'), 'wb'))

print("Artifacts created successfully!")