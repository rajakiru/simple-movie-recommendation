import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_recommendations(movie, num_recommendations):
    idx = movies[movies['original_title'] == movie].index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations]
    # Top 10 similar items (excluding itself)
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in sim_scores:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].original_title)
    return recommended_movie_names, recommended_movie_posters

st.header('Kiru: Movie Recommendation System')
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['original_title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)
num_recommendations = st.slider('Number of recommendations', min_value=1, max_value=20, value=10)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = get_recommendations(selected_movie, num_recommendations + 1)
    
    if recommended_movie_names and recommended_movie_posters:
        for i in range(0, len(recommended_movie_names)+1, 5):
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                if i + idx < len(recommended_movie_names):
                    col.text(recommended_movie_names[i + idx])
                    col.image(recommended_movie_posters[i + idx])
    else:
        st.warning("No recommendations to display.")
