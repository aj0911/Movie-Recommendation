import pickle
import streamlit as st
import pandas as pd
import requests

movie_list = pickle.load(open('movies_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
df = pd.DataFrame(movie_list);

def fetchMoviePoster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommendMovies(movie_title):
    recommended_movie_names = []
    recommended_movie_poster = []
    movieIndex = df[df['original_title']== movie_title].index[0]
    pred_arr = sorted(list(enumerate(similarity[movieIndex])),key=lambda x:x[1],reverse=True)[0:5]
    for i in pred_arr:
        recommended_movie_poster.append(fetchMoviePoster(df.iloc[i[0]]['id']))
        recommended_movie_names.append(df.iloc[i[0]]['original_title'])
    return recommended_movie_names,recommended_movie_poster;

st.header('Movie Recommender App')


selected_movie = st.selectbox("Type or select a movie from the dropdown",df['original_title'].values)

if st.button('Search'):
    recommended_movie_names,recommended_movie_posters = recommendMovies(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5,gap='small')
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

