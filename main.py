import pandas as pd
import streamlit as st
import pickle
import requests
from dotenv.main import load_dotenv
import os

load_dotenv()
api = os.environ['API_KEY']
print(api)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id,api)
    print("My api "  + url )
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_name = []
    recommended_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_poster.append(fetch_poster(movie_id))
        recommended_name.append(movies.iloc[i[0]].title)
    return recommended_name,recommended_poster

movies_list = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender")

option = st.selectbox('check the results here',
movies['title'].values)

if st.button('Recommend'):
    recommended_name, recommended_poster = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_name[0])
        st.image(recommended_poster[0])
    with col2:
        st.text(recommended_name[1])
        st.image(recommended_poster[1])

    with col3:
        st.text(recommended_name[2])
        st.image(recommended_poster[2])
    with col4:
        st.text(recommended_name[3])
        st.image(recommended_poster[3])
    with col5:
        st.text(recommended_name[4])
        st.image(recommended_poster[4])
