"""
A Universal connection function that connects to a postgres database and returns the connection object.
"""

import psycopg2
import streamlit as st


def connect():
    conn = psycopg2.connect(
        dbname=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
    )
    return conn
