import streamlit as st
from streamlit_option_menu import option_menu
import pickle

from recommend import *
from explore import *
from home import *
from db_conn import connect


@st.cache_resource(ttl=3600)
def load_data():
    conn = None
    try:
        conn = connect()
        with open("../Model/top_recomm_idx.pkl", "rb") as f:
            top_recomm_idx = pickle.load(f)
        return conn, top_recomm_idx
    except Exception as e:
        st.header(e)
        if conn is not None:
            conn.close()


def main():

    page_selection = option_menu(
        menu_title=None,
        options=["Home", "Recommendations", "Explore Movies"],
        icons=["house", "robot", "search", "info"],
        default_index=0,
        orientation="horizontal",
    )

    if "data_loaded" not in st.session_state:
        st.session_state.data = load_data()
        st.session_state.data_loaded = True

    conn = st.session_state.data[0]

    if page_selection == "Home":
        home()

    elif page_selection == "Recommendations":

        top_recommendations = st.session_state.data[1]

        recomm(conn, top_recommendations)

    elif page_selection == "Explore Movies":
        explore(conn)


if __name__ == "__main__":
    main()
