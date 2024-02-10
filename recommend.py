import streamlit as st
from recomm_helper import *


def recomm(_conn, top_recommendations):

    cur = _conn.cursor()

    st.title("Movie Recommender! 🤖")

    cur.execute("SELECT revised_title FROM detailed;")

    movie_titles = [row[0] for row in cur.fetchall()]

    unique_genres, unique_countries, unique_languages, unique_popularity = get_unique(
        cur
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        selected_movie = st.selectbox(
            "Type or select a movie and optionally set the filters on the sidebar",
            [""] + movie_titles,
            index=0,
        )

    with col2:
        st.write("")
        st.write("")
        generate_button = st.button("Generate")

    st.sidebar.subheader("Filters")

    num_recommendations = st.sidebar.number_input(
        "Number of Recommendations",
        help="Select number of recommendations to show (max 100)",
        min_value=1,
        max_value=100,
        value=10,
    )

    selected_genres = st.sidebar.multiselect(
        "Genres",
        ["All"] + unique_genres,
        help="Select multiple genres (max 3)",
        default=["All"],
    )
    if len(selected_genres) > 3 or not selected_genres:
        st.error("Please select minimum 1 and up to 3 genres only.")

    selected_vote = st.sidebar.number_input(
        "Minimum rating",
        help="Select minimum movie vote average (0-9)",
        min_value=0,
        max_value=9,
        value=0,
    )

    selected_popularity = st.sidebar.selectbox(
        "Popularity",
        ["All"] + unique_popularity,
        index=0,
        help="Select the exact popularity level",
    )

    selected_year = st.sidebar.number_input(
        "Released in/after",
        help="Select minimum movie release year (2000-2017)",
        min_value=2000,
        max_value=2017,
        value=2000,
    )

    selected_countries = st.sidebar.multiselect(
        "Countries",
        ["All"] + unique_countries,
        help="Select multiple countries (max 3)",
        default=["All"],
    )
    if len(selected_countries) > 3 or not selected_countries:
        st.error("Please select minimum 1 and up to 3 countries.")

    selected_languages = st.sidebar.multiselect(
        "Languages",
        ["All"] + unique_languages,
        help="Select multiple languages (max 3)",
        default=["All"],
    )
    if len(selected_languages) > 3 or not selected_languages:
        st.warning("Please select minimum 1 and up to 3 languages.")

    if selected_movie != "" and generate_button:

        movie_ids = return_recommendations2(
            selected_movie,
            top_recommendations,
            cur,
            num_recommendations,
            selected_countries,
            selected_genres,
            selected_languages,
            selected_popularity,
            selected_vote,
            selected_year,
        )

        display_movies(movie_ids, cur)

    cur.close()
