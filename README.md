# 🎬 Content-Based Movie Recommender System

A streamlined web application that delivers **personalized movie recommendations** using content similarity. It analyzes metadata like **genres, keywords, cast, and director** to recommend movies with similar thematic DNA.

🔗 [Live Demo on Render](https://movies-recommender-system-enom.onrender.com/)  
📂 [GitHub Repository](https://github.com/aniruddhapal/movies-recommender-system)

---

## 📌 Table of Contents
- [Overview](#-overview)
- [Dataset](#-dataset)
- [How It Works](#-how-it-works)
- [Key Features](#-key-features)
- [Technical Challenges & Solutions](#-technical-challenges--solutions)
- [Project Structure](#-project-structure)
- [How to Run Locally](#-how-to-run-locally)
- [Deployment](#-deployment)
- [Limitations](#-limitations)
- [Credits](#-credits)

---

## 🧠 Overview

This project builds a **content-based filtering system** that recommends movies similar to a selected one. Instead of relying on user ratings, it evaluates the **textual and categorical attributes** of movies to find thematic matches.

---

## 📊 Dataset

- **Source**: [TMDB 5000 Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- Files Used:
  - `tmdb_5000_movies.csv`
  - `tmdb_5000_credits.csv`

### Preprocessing Steps
- Merged datasets on the `title` column.
- Removed null `overview` rows.
- Extracted key fields from JSON-like columns:
  - Top 3 cast members.
  - Director from crew.
  - All keywords and genres.
- Combined these into a single text "tag" per movie.
- Standardized text: lowercase, joined multi-word tokens (e.g., `sciencefiction`), and applied **lemmatization** via NLTK.

---

## ⚙️ How It Works

### Vectorization & Similarity
- **Vectorizer**: `CountVectorizer` on top 3000 words.
- **Similarity Metric**: `cosine_similarity` from `sklearn.metrics.pairwise`.

### Recommendation Logic
1. User selects a movie.
2. Top 5 similar movies are fetched based on cosine similarity of tags.
3. Movie posters are pulled via TMDB API.

---

## ⭐ Key Features

- Real-time content-based recommendations.
- Highly modular pipeline.
- Fully optimized for free-tier deployment (≤512 MB RAM).
- Poster fetching via TMDB API.
- UI powered by Streamlit.

---

## 🧩 Technical Challenges & Solutions

| Problem | Solution |
|--------|----------|
| `ConnectionResetError` from TMDB API | Used `@st.cache_data` to cache responses and reduce load |
| Large file size (`similarity.pkl` > 100MB) | Removed from Git history and rebuilt during deployment |
| RAM exceeded during live serving | Compressed matrix from 176MB to 65MB by reducing vocab and using `float32` |
| CI/CD deployment issues on Render | Configured build to recreate artifacts on every push |

---

## 🗂 Project Structure

movies-recommender-system/
├── data/ # Raw TMDB datasets
├── artifacts/ # Generated model artifacts (ignored in Git)
├── create_artifacts.py # Pipeline: preprocessing + vectorization + save
├── app.py # Streamlit UI for serving recommendations
├── requirements.txt # Dependencies
└── .gitignore # Ignore artifacts and caches


### Modularity

- `create_artifacts.py`: One-time computation pipeline.
- `app.py`: Lightweight UI that loads precomputed artifacts.
- CI/CD friendly: artifacts rebuilt during deployment—not stored in repo.

---

## 🖥 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/aniruddhapal/movies-recommender-system.git
cd movies-recommender-system

# Install dependencies
pip install -r requirements.txt

# Generate artifacts
python create_artifacts.py

# Run the app
streamlit run app.py

🚀 Deployment
Framework: Streamlit
Host: Render (Free Tier)
CI/CD: Auto-deploy on git push to main.
Build steps:
  Install dependencies
  Download NLTK data
  Run create_artifacts.py

⚠️ Limitations
- Only supports movies from the TMDB 5000 dataset.
- Recommender may underperform for niche or very obscure titles.
- No user-specific personalization—no collaborative filtering.

👏 Credits
- TMDB Dataset on Kaggle
- TMDB API for poster data

Inspired by common NLP preprocessing and recommender system practices.

