import streamlit as st
from explore_helper import *
import datetime


def explore(_conn):

    cur = _conn.cursor()

    st.title("Explore Movies 🔎")
    st.subheader("Enter only the necessary movie filters")

    (
        unique_genres,
        unique_countries,
        unique_languages,
        unique_popularity,
        unique_keywords,
        unique_casts,
        unique_crews,
        unique_companies,
    ) = get_unique(cur)

    col1A, col1B = st.columns([1, 1])
    with col1A:
        selected_keywords = st.multiselect(
            "Keywords",
            unique_keywords,
            help="Select multiple keywords",
        )
    with col1B:
        selected_genres = st.multiselect(
            "Genres",
            unique_genres,
            help="Select multiple genres",
        )

    col2A, col2B, col2C = st.columns([1, 1, 1])
    with col2A:
        selected_cast = st.selectbox(
            "Cast", [""] + unique_casts, help="Select single cast", index=0
        )
    with col2B:
        selected_crew = st.selectbox(
            "Crew", [""] + unique_crews, help="Select single crew", index=0
        )
    with col2C:
        selected_company = st.selectbox(
            "Production Company",
            [""] + unique_companies,
            help="Select single production company",
            index=0,
        )

    col3A, col3B = st.columns([1, 1])
    with col3A:
        selected_country = st.selectbox(
            "Production Country",
            [""] + unique_countries,
            help="Select single production country",
            index=0,
        )
    with col3B:
        selected_language = st.selectbox(
            "Movie Language",
            [""] + unique_languages,
            help="Select single language",
            index=0,
        )

    col4A, col4B = st.columns([1, 1])
    with col4A:
        selected_startdate = st.date_input(
            "Release Date [lower limit]",
            format="MM/DD/YYYY",
            min_value=datetime.date(2000, 1, 1),
            max_value=datetime.date(2020, 1, 1),
            value=datetime.date(2000, 1, 1),
            help="Select lower limit to movie release date",
        )
    with col4B:
        selected_enddate = st.date_input(
            "Release Date [upper limit]",
            format="MM/DD/YYYY",
            min_value=datetime.date(2000, 1, 1),
            max_value=datetime.date(2020, 1, 1),
            value=datetime.date(2020, 1, 1),
            help="Select upper limit to movie release date",
        )

    st.sidebar.subheader("Additional Filters")

    num_recommendations = st.sidebar.number_input(
        "Number of Recommendations",
        help="Select number of recommendations to show (1-150)",
        min_value=1,
        max_value=150,
        value=15,
    )

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

    selected_runtime = st.sidebar.number_input(
        "Minimum Runtime (in minutes)",
        min_value=0,
        value=0,
        max_value=500,
        help="Select the minimum runtime in minutes (0-500)",
    )

    st.sidebar.subheader("Sort")
    sorting_options = {
        "Vote Average (Ascending)": "detailed.vote_average ASC",
        "Vote Average (Descending)": "detailed.vote_average DESC",
        "Popularity (Ascending)": "detailed.popularity ASC",
        "Popularity (Descending)": "detailed.popularity DESC",
        "Runtime (Ascending)": "detailed.runtime ASC",
        "Runtime (Descending)": "detailed.runtime DESC",
    }

    selected_sorting = st.sidebar.selectbox(
        "Sort by:",
        [""] + list(sorting_options.keys()),
        index=0,
        help="Select ascending/descending results",
    )

    query = generate_query(
        selected_keywords,
        selected_genres,
        selected_cast,
        selected_crew,
        selected_company,
        selected_country,
        selected_language,
        selected_startdate,
        selected_enddate,
        num_recommendations,
        selected_vote,
        selected_popularity,
        selected_runtime,
        selected_sorting,
        sorting_options,
    )

    cur.execute(query)
    rows = cur.fetchall()

    _, col1, col2, _ = st.columns([3, 2, 2, 3])
    with col1:
        query_button = st.button(
            label="Show query",
            help="Press button to show the database query for selected filters",
        )
    with col2:
        apply_button = st.button(
            label="Apply all Filters", help="Press button to show filtered movies"
        )

    if query_button:
        st.code(query, language="sql")
    if apply_button:
        display_movies([row[0] for row in rows], cur)

    cur.close()
