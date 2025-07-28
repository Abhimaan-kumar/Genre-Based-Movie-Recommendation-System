import streamlit as st
import pandas as pd
import requests
import pickle 

# Function to fetch poster using TMDB API
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=16f2918def5814f34502019f73334553&language=en-US'
    )
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Function to recommend movies by genre
def recommend_by_genre(genre, movies_df, top_n=5):
    genre_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)].drop_duplicates()
    return genre_movies.head(top_n)

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict) # Must have 'title', 'genres', 'id'
movies.columns = movies.columns.str.lower()  # Normalize column names


# UI
st.title("🎬 Genre-Based Movie Recommender System")

genre_input = st.selectbox("Choose a genre", 
    ['Select one','Comedy', 'Animation', 'Documentary', 'Foreign', 'TV Movie', 'Mystery', 'Fantasy', 'ScienceFiction', 'Crime', 'War', 'Romance', 'Thriller', 'Adventure', 'Music', 'Western', 'Drama', 'Horror', 'History', 'Family', 'Action']
)

if genre_input != 'Select one' and st.button("Recommend"):
    recommended = recommend_by_genre(genre_input, movies)
    cols = st.columns(5)

    for i in range(len(recommended)):
        with cols[i % 5]:  # Loop over columns safely
            st.text(recommended.iloc[i].title)
            st.image(fetch_poster(recommended.iloc[i].id))