import streamlit as st
import pickle
import requests
import pandas as pd
from image_url import poster_path
from app import return_saved

st.set_page_config(layout="wide")

saved=return_saved()
    
movies=saved["movies"]

st.title("Movie Recommendation System 🎬🍿")
st.divider()

movies_list=movies["title"]


selected_movie=st.selectbox(label="Select a Movie",options=movies_list,index=None)
recommended_movies=None

if st.button("Get Recommendations"):
    with st.spinner("finding your recommendations..."):
        if selected_movie is not None:
            
            movie_id = int(movies[movies["title"] == selected_movie]["id"].iloc[0])

            url="http://localhost:8000/recommend"

            data={
                "id":movie_id
            }

            response=requests.post(url,json=data)

            recommended_movies=response.json()
            
        col0,col1,col2,col3,col4=st.columns(5)

        cols=[col0,col1,col2,col3,col4]
            
        if recommended_movies is not None:
            image_urls=[]
            movie_names=[]
            for movie in recommended_movies:
                image_urls.append(poster_path(movie))
                movie_names.append(movie)
                
            for idx in range(len(image_urls)):
                
                current_col=idx%5
                with cols[current_col]:
                    with st.container(width="content"):
                        
                        if image_urls[idx]:
                                
                            st.text(movie_names[idx],text_alignment="center")
                            st.image(image_urls[idx])
                            
                        else:
                            st.text(movie_names[idx],text_alignment="center")
                            st.image("images.png",width=400)
            



