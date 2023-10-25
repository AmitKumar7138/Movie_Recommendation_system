import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    recommended_movies = []
    recommended_movies_posters = []
    m_index = movies_list[movies_list['title'] == movie].index[0]
    cos_distances = similarity_metrics[m_index]
    indexes = sorted(list(enumerate(cos_distances)),
                     key=lambda x: x[1], reverse=True)[1:6]

    for i in indexes:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_list)
movies_list2 = movies_list['title'].values
similarity_metrics = pickle.load(open('similarity_metrics.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select your movie', movies_list2
)
print(selected_movie_name)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0], width=140)

    with col2:
        st.text(names[1])
        st.image(posters[1], width=140)

    with col3:
        st.text(names[2])
        st.image(posters[2], width=140)

    with col4:
        st.text(names[3])
        st.image(posters[3], width=140)

    with col5:
        st.text(names[4])
        st.image(posters[4], width=140)
