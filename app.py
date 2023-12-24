import streamlit as st 
import pandas as pd 
import pickle
import requests

st.title("Movie Recommender System")

final_df=pd.DataFrame(pickle.load(open("movies.pkl","rb")))
closeness=pickle.load(open("closeness.pkl","rb"))


def fetch_poster(movie_id):
     response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2400009d27b7a556986706cc19ccd4ab&language=en-US')
     data=response.json()
     return "https://image.tmdb.org/t/p/w342"+data['poster_path']
     

def recommend(movie):
   movie_index=final_df[final_df['title']==movie].index[0]
   distance=closeness[movie_index]
   movies_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

   recommend_movies_list=[]
   recommend_movies_posters=[]
   for i in movies_list:
        movie_id=final_df.iloc[i[0]].id
        
        recommend_movies_list.append(final_df.iloc[i[0]].title)
        #fetching poster from imdb api
        recommend_movies_posters.append(fetch_poster(movie_id))
   return recommend_movies_list,recommend_movies_posters

options=final_df["title"].values

selected_option = st.selectbox(
    'Select the movie name that suits your mood?',options)



def main():
        if st.button("Recommend"):
            names,posters=recommend(selected_option)
            col1, col2, col3 ,col4 , col5 = st.columns(5)

            with col1:
                
                st.image(posters[0])
                st.write(names[0])

            with col2:
                
                st.image(posters[1])
                st.write(names[1])

            with col3:
                
                st.image(posters[2])
                st.write(names[2])

            with col4:
                
                st.image(posters[3])
                st.write(names[3])

            with col5:
                
                st.image(posters[4])
                st.write(names[4])



with open("movie.css") as s:
    st.markdown(f"<style>{s.read()}</style>",unsafe_allow_html=True)

main()



