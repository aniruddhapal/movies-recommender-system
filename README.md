# 1. Project Basics
## Project Title: Content-Based Movie Recommender System
## Description: A web application that provides personalized movie recommendations. It suggests films based on content similarity, analyzing attributes like genre, keywords, cast, and director to find movies with similar thematic DNA.

### Deployed App Link: https://movies-recommender-system-enom.onrender.com
### GitHub Repo Link: https://github.com/aniruddhapal/movies-recommender-system

# 2. Technical Details
## Dataset Used: TMDB 5000 Movie Dataset from Kaggle.
### Preprocessing:
- Two separate datasets (tmdb_5000_movies.csv and tmdb_5000_credits.csv) were merged on the 'title' column.
- Handled missing values by dropping a few rows with null overviews.
- **Feature Engineering**: Parsed JSON-like string columns (genres, keywords, cast, crew) to extract key textual information. For instance, extracted the top 3 cast members and the director's name.
- Created a unified "tags" corpus for each movie by concatenating the overview, genres, keywords, top cast, and director.
- **Text Normalization**: Standardized the text data by converting it to lowercase, removing spaces from multi-word tags (e.g., "Science Fiction" -> "sciencefiction") to treat them as single entities, and applying      **lemmatization** using NLTK to reduce words to their root form (e.g., "actions", "acting" -> "action").
### Model(s) Used:
- This is a purely **Content-Based Filtering model**.
- **Vectorization**: Used sklearn.feature_extraction.text.CountVectorizer to convert the text "tags" for each movie into a high-dimensional vector space. The vocabulary was optimized to the top 3,000 most frequent   words to ensure performance on a resource-constrained server.
- **Similarity Metric**: Employed sklearn.metrics.pairwise.cosine_similarity to calculate the similarity score between every pair of movie vectors. A higher cosine similarity score indicates a greater thematic resemblance.
### Evaluation Metrics:
- As this is an unsupervised recommendation model, traditional metrics like RMSE or accuracy are not applicable.
- Evaluation was performed **qualitatively** by testing well-known movies and assessing the relevance and coherence of the top 5 recommended movies. The goal was to ensure the recommendations were logical and contextually appropriate (e.g., recommending other sci-fi epics for "Avatar").
### Key Performance Results:
- The model successfully generates contextually relevant movie recommendations in real-time.
- Memory Optimization: The final similarity.pkl artifact was optimized from **~176** MB down to **~65** MB by reducing the feature vocabulary from 5000 to 3000 and changing the data type from float64 to float32. This was a critical step that enabled deployment on a free-tier server with a 512 MB RAM limit.
### Major Challenges Faced:
 1. Deployment Network Errors: Initial deployment was plagued by inconsistent ConnectionResetError issues when fetching posters from the TMDB API. This was diagnosed as a combination of a strict local firewall and aggressive server-side rate-limiting. **Resolved by implementing a robust caching strategy** using Streamlit's @st.cache_data decorator, which drastically reduced API calls.
 2. Git Version Control for Large Files: The 176 MB similarity matrix exceeded GitHub's 100 MB file size limit. Initial attempts to use Git LFS failed due to free-tier bandwidth quotas. **Resolved by completely rewriting the Git history** to purge the large file, adopting a CI/CD-friendly approach where artifacts are built during deployment rather than being stored in version control.
 3. Resource Exhaustion on a Live Server: The deployed application initially crashed due to exceeding the 512 MB RAM limit of the free hosting tier. **Resolved by performing aggressive memory optimization** on the similarity matrix, as detailed in the performance results.
### Deployment Stack:
**Framework**: Streamlit
**Hosting Platform**: Render (Free Tier)
**CI/CD**: The deployment pipeline was configured on Render to be triggered automatically on every git push to the main branch. The build process installs dependencies, downloads NLTK data, and runs the artifact generation script.
# 3. Code Structure
The project follows a modular structure that cleanly separates the one-time data processing pipeline from the live web application.
## Key Folders/Scripts:
- data/: Contains the raw .csv datasets.
- artifacts/: Contains the pre-computed model artifacts (movies_list.pkl, similarity.pkl). This folder is generated during the build and is included in .gitignore.
- create_artifacts.py: **The Data Processing Pipeline**. A standalone script that loads raw data, performs all cleaning, feature engineering, text processing, vectorization, and similarity calculation, and saves the  final artifacts to the artifacts/ folder.
- app.py: **The Web Application.** A Streamlit script that serves as the user interface. It does **no data processing**. It simply loads the pre-computed artifacts from the artifacts/ folder and uses them to serve recommendations quickly.
- requirements.txt: Lists all Python dependencies for the project.
- .gitignore: Specifies which files and folders (like artifacts/ and __pycache__/) should be excluded from Git version control.
## Modularity:
The project is highly modularized. The data processing pipeline (create_artifacts.py) is completely decoupled from the prediction/serving application (app.py). This is a best practice that allows for independent development and makes the live application lightweight and fast, as all heavy computation is done beforehand.
