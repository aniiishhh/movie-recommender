"""
Helper function implementation for the Explore Movies Section.
"""

import streamlit as st


@st.cache_data(ttl=3600)
def get_unique(_cur):

    _cur.execute("SELECT DISTINCT unnest(genres) FROM filters;")
    unique_genres = _cur.fetchall()
    unique_genres = [genre[0] for genre in unique_genres]

    _cur.execute("SELECT DISTINCT unnest(production_countries) FROM filters;")
    unique_countries = _cur.fetchall()
    unique_countries = [country[0] for country in unique_countries]

    _cur.execute("SELECT DISTINCT original_language FROM filters;")
    unique_languages = _cur.fetchall()
    unique_languages = [language[0] for language in unique_languages]

    _cur.execute("SELECT DISTINCT popularity_category FROM filters;")
    unique_popularity = _cur.fetchall()
    unique_popularity = [popularity[0] for popularity in unique_popularity]

    _cur.execute("SELECT DISTINCT unnest(keywords) FROM detailed;")
    unique_keywords = _cur.fetchall()
    unique_keywords = [keyword[0] for keyword in unique_keywords]

    _cur.execute("SELECT DISTINCT unnest(casts) FROM detailed;")
    unique_casts = _cur.fetchall()
    unique_casts = [cast[0] for cast in unique_casts]

    _cur.execute("SELECT DISTINCT unnest(crew) FROM detailed;")
    unique_crews = _cur.fetchall()
    unique_crews = [crew[0] for crew in unique_crews]

    _cur.execute("SELECT DISTINCT unnest(production_companies) FROM detailed;")
    unique_companies = _cur.fetchall()
    unique_companies = [company[0] for company in unique_companies]

    return (
        unique_genres,
        unique_countries,
        unique_languages,
        unique_popularity,
        unique_keywords,
        unique_casts,
        unique_crews,
        unique_companies,
    )


def generate_query(
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
    sorting_dict,
):

    query = """SELECT detailed.*, filters.*
            FROM filters
            INNER JOIN detailed ON detailed.id = filters.movie_id
            WHERE 1 = 1
            """

    if selected_keywords:
        keywords_condition = " AND ARRAY[{}] <@ detailed.keywords".format(
            ", ".join(["'{}'".format(k) for k in selected_keywords])
        )
        query += keywords_condition

    if selected_genres:
        keywords_condition = " AND ARRAY[{}] <@ filters.genres".format(
            ", ".join(["'{}'".format(k) for k in selected_genres])
        )
        query += keywords_condition

    if selected_cast:
        cast_condition = " AND '{}' = ANY(detailed.casts)".format(selected_cast)
        query += cast_condition

    if selected_crew:
        crew_condition = " AND '{}' = ANY(detailed.crew)".format(selected_crew)
        query += crew_condition

    if selected_company:
        company_condition = " AND '{}' = ANY(detailed.production_companies)".format(
            selected_company
        )
        query += company_condition

    if selected_country:
        country_condition = " AND '{}' = ANY(filters.production_countries)".format(
            selected_country
        )
        query += country_condition

    if selected_language:
        language_condition = " AND '{}' = filters.original_language".format(
            selected_language
        )
        query += language_condition

    if selected_startdate:
        startdate_condition = " AND detailed.release_date >= '{}'".format(
            selected_startdate
        )
        query += startdate_condition

    if selected_enddate:
        enddate_condition = " AND detailed.release_date <= '{}'".format(
            selected_enddate
        )
        query += enddate_condition

    vote_condition = " AND detailed.vote_average >= {}".format(selected_vote)
    query += vote_condition

    if selected_popularity != "All":
        popularity_condition = " AND filters.popularity_category = '{}'".format(
            selected_popularity
        )
        query += popularity_condition

    runtime_condition = " AND detailed.runtime >= {}".format(selected_runtime)
    query += runtime_condition

    if selected_sorting:
        query += " ORDER BY {}".format(sorting_dict[selected_sorting])

    query += " LIMIT {};".format(num_recommendations)

    return query


def display_movies(movie_ids, cur):
    if not movie_ids:
        st.write("No movies to display on this page. Please try changing the filters.")
    else:
        movie_url = "https://www.themoviedb.org/movie/"
        st.balloons()
        st.write("Filtered Results: ")
        for i in range(0, len(movie_ids), 3):
            col1, col2, col3 = st.columns(3)

            with col1:
                if i < len(movie_ids):
                    movie_id = movie_ids[i]
                    cur.execute("SELECT * FROM detailed WHERE id = %s;", (movie_id,))
                    movie_row = cur.fetchone()

                    if movie_row:
                        poster_path = movie_row[16]
                        if poster_path:
                            st.image(poster_path, width=200)
                        else:
                            st.image("no-poster-available.jpg", width=200)
                        st.markdown(f"[{movie_row[12]}]({movie_url}{movie_id})")
            with col2:
                if i + 1 < len(movie_ids):
                    movie_id = movie_ids[i + 1]
                    cur.execute("SELECT * FROM detailed WHERE id = %s;", (movie_id,))
                    movie_row = cur.fetchone()

                    if movie_row:
                        poster_path = movie_row[16]
                        if poster_path:
                            st.image(poster_path, width=200)
                        else:
                            st.image("no-poster-available.jpg", width=200)
                        st.markdown(f"[{movie_row[12]}]({movie_url}{movie_id})")

            with col3:
                if i + 2 < len(movie_ids):
                    movie_id = movie_ids[i + 2]
                    cur.execute("SELECT * FROM detailed WHERE id = %s;", (movie_id,))
                    movie_row = cur.fetchone()

                    if movie_row:
                        poster_path = movie_row[16]
                        if poster_path:
                            st.image(poster_path, width=200)
                        else:
                            st.image("no-poster-available.jpg", width=200)
                        st.markdown(f"[{movie_row[12]}]({movie_url}{movie_id})")
