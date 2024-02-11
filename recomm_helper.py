"""
Helper function implementation for the Recommendations Section.
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

    return unique_genres, unique_countries, unique_languages, unique_popularity


def get_recommendations(title, recomm_dict, cur, n=10):
    cur.execute("SELECT idx FROM detailed WHERE revised_title = %s;", (title,))
    idx = cur.fetchone()[0]

    top_indices = recomm_dict[idx][1 : n + 1]

    recommended_titles = []
    for index in top_indices:
        cur.execute("SELECT revised_title FROM detailed WHERE idx = %s;", (index,))
        recommended_title = cur.fetchone()[0]
        recommended_titles.append(recommended_title)

    st.write(f"Top {n} recommendations for '{title}':")
    for i, recommended_title in enumerate(recommended_titles, 1):
        st.write(f"{i}. {recommended_title}")


def return_recommendations(
    title, recomm_dict, cur, n, countries, genres, languages, popularity, vote, year
):

    cur.execute(
        "SELECT idx, poster_path FROM detailed WHERE revised_title = %s;", (title,)
    )
    row = cur.fetchone()
    idx = row[0]
    poster_path = row[1]

    _, col2, _ = st.columns([1, 4, 1])

    with col2:
        st.subheader(title)
        if poster_path:
            st.image(poster_path, width=300)
        else:
            st.image("./Images/no-poster-available.jpg", width=300)

    top_indices = []

    for idx in recomm_dict[idx][1:]:
        cur.execute("SELECT * FROM filters WHERE idx = %s;", (idx,))
        movie_data = cur.fetchone()

        if movie_data:
            if (
                (genres == ["All"] or any(genre in movie_data[3] for genre in genres))
                and (languages == ["All"] or movie_data[4] in languages)
                and (
                    countries == ["All"]
                    or any(country in movie_data[5] for country in countries)
                )
                and (not year or movie_data[6] >= year)
                and (not vote or movie_data[7] >= vote)
                and (popularity == "All" or movie_data[8] == popularity)
            ):
                top_indices.append(idx)

        if len(top_indices) >= n:
            break

    movie_ids = []

    for idx in top_indices:
        cur.execute("SELECT id FROM detailed WHERE idx = %s;", (idx,))
        movie_id = cur.fetchone()[0]
        movie_ids.append(movie_id)

    return movie_ids


####################################################################################################


def return_recommendations2(
    title, recomm_dict, cur, n, countries, genres, languages, popularity, vote, year
):
    cur.execute(
        "SELECT idx, poster_path FROM detailed WHERE revised_title = %s;", (title,)
    )
    row = cur.fetchone()
    idx = row[0]
    poster_path = row[1]

    _, col2, _ = st.columns([1, 4, 1])

    with col2:
        st.subheader(title)
        if poster_path:
            st.image(poster_path, width=300)
        else:
            st.image("./Images/no-poster-available.jpg", width=300)

    all_recomm_idx_tuple = tuple(recomm_dict[idx][1:])
    cur.execute("""SELECT * FROM filters WHERE idx IN %s""", (all_recomm_idx_tuple,))
    all_recomm_rows = cur.fetchall()

    idx_row_dict = {row[1]: row for row in all_recomm_rows}

    ordered_rows = []
    for idx_value in recomm_dict[idx][1:]:
        ordered_rows.append(idx_row_dict[idx_value])

    top_indices = return_filtered_rows(
        ordered_rows, n, countries, genres, languages, popularity, vote, year
    )

    filtered_idx_tuple = tuple(top_indices)
    cur.execute(
        """SELECT movie_id, idx FROM filters WHERE idx IN %s""", (filtered_idx_tuple,)
    )
    filtered_rows = cur.fetchall()

    idx_row_dict = {row[1]: row for row in filtered_rows}

    final_lst = []
    for idx_value in recomm_dict[idx][1:]:
        if idx_value in idx_row_dict:
            final_lst.append(idx_row_dict[idx_value][0])

    return final_lst


def return_filtered_rows(rows, n, countries, genres, languages, popularity, vote, year):
    top_indices = []
    for movie_data in rows:
        if (
            (genres == ["All"] or any(genre in movie_data[3] for genre in genres))
            and (languages == ["All"] or movie_data[4] in languages)
            and (
                countries == ["All"]
                or any(country in movie_data[5] for country in countries)
            )
            and (not year or movie_data[6] >= year)
            and (not vote or movie_data[7] >= vote)
            and (popularity == "All" or movie_data[8] == popularity)
        ):
            top_indices.append(movie_data[1])

        if len(top_indices) >= n:
            break

    return top_indices


####################################################################################################


def display_movies(movie_ids, cur):
    if not movie_ids:
        st.write("No movies to display on this page.")
    else:
        movie_url = "https://www.themoviedb.org/movie/"
        st.balloons()
        st.write("Recommendations: ")
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
                            st.image("./Images/no-poster-available.jpg", width=200)
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
                            st.image("./Images/no-poster-available.jpg", width=200)
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
                            st.image("./Images/no-poster-available.jpg", width=200)
                        st.markdown(f"[{movie_row[12]}]({movie_url}{movie_id})")
