"""
The Home Section.
"""

import streamlit as st


def home():
    st.title("The Movie Recommendation App!")
    st.write(
        "Welcome to Movie Recommender, your ultimate destination for discovering new movies and exploring vast collections of cinematic treasures. This app utilizes cutting-edge technology to bring you personalized movie recommendations and advanced filtering options to cater to your unique tastes."
    )
    st.write("")
    st.image("home_collage.jpg")
