import streamlit as st
import pandas as pd
import pickle
import requests
from api_key import API_KEY

API=API_KEY

#importing pickle files
movies = pickle.load(open('movies.pkl', 'rb'))
similarity_mat=pickle.load(open('similarity.pkl', 'rb'))

import requests
import streamlit as st

# Function to fetch posters for the recommended movies
def get_poster(movie_id):
    API = "your_api_key_here"  # Replace with your actual API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={API}"
    response = requests.get(url)
    data = response.json()

    # Check if 'posters' key exists and has at least one item
    if 'posters' in data and len(data['posters']) > 0:
        # Get the poster's file path
        poster_path = data['posters'][0]['file_path']
        return "https://image.tmdb.org/t/p/w500" + poster_path
    else:
        # Return a placeholder image if no posters are found
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

# Recommendation system function
def recommendMovie(movie):
    # Fetch movie index from title
    movie_index = movies[movies['title'] == movie].index[0]

    # Fetch similarity scores
    distances = similarity_mat[movie_index]

    # Fetch the indices of the top 5 similar movies
    similar_movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    # Fetch posters and title for the movies
    similar_movies_title = []
    similar_movies_poster = []
    for i in similar_movie_list:
        # Fetch title of similar movies
        similar_movies_title.append(movies.iloc[i[0]].title)

        # Fetch poster
        poster_url = get_poster(movies.iloc[i[0]].movie_id)
        similar_movies_poster.append(poster_url)

    return similar_movies_poster, similar_movies_title

# Streamlit app
st.title("Movie Recommendation System")
st.write("This is a simple movie recommendation system that recommends movies based on user input.")

movie_selected = st.selectbox(
    "Select a movie",
    movies.title,
)
if st.button("Recommend"):
    # Find similar movies
    similar_movies_poster, similar_movies_title = recommendMovie(movie_selected)
    for i in range(len(similar_movies_title)):
        st.image(similar_movies_poster[i], width=200)
        st.write(similar_movies_title[i])

#   col1, col2, col3 = st.columns(3)
  
#   with col1:
#     st.image(similar_movies_poster[0])
#     st.write(similar_movies_title[0])

#   with col2:
#     st.image(similar_movies_poster[1])
#     st.write(similar_movies_title[1])

#   with col3:
#     st.image(similar_movies_poster[2])
#     st.write(similar_movies_title[2])
#   st.write("You might also like:")
#   for i in range(len(similar_movies_title)):
#         st.image(similar_movies_poster[i], caption=similar_movies_title[i], width=200)


