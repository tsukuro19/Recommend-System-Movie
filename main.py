import streamlit as st 
import pickle
import pandas as pd

import requests

# Hàm lấy API từ TheMovieDB
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2694d06e3826a88148f267daaf6734af&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
# Hàm đề xuất--------------------------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id 
        
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API lấy api gắn vô chắc tầm 30 phút
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster
#---------------------------------------------------------------------
    
# vì main.py và file load tên movie lên combox phải cùng một nơi
#=> Tạm thời: copy file movie_trained.pkl :))) ra cùng chỗ main.py
movies_dict = pickle.load(open('movie_trained.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# làm tương tự với file similary.pkl
similarity = pickle.load(open('similary_trained.pkl','rb'))

# sử dụng title của thư viện streamlit 
st.title("Movie recommender system Nhóm 9_AI")

# sử dụng combobox của thư viện streamlit
# Cải thiện combox xổ xuống thay vì xổ lên
selected_movie_name = st.selectbox(
    "How would you to be contacted?",
movies['title'].values)  # Sửa ở đây

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    
    # for i in recommendations:
    #     st.write(i)
