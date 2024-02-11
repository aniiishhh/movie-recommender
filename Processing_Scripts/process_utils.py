"""
Contains utility functions used throughout the processing scripts.
"""

import pandas as pd
import nltk
import numpy as np
import requests
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

nltk.download("wordnet")
nltk.download("punkt")
nltk.download("stopwords")


def process_list_elements(lst, strip_whitespace=True, lowercase=True):
    processed_list = []

    for element in lst:
        if strip_whitespace:
            element = element.replace(" ", "")
        if lowercase:
            element = element.lower()
        processed_list.append(element)

    return processed_list


def preprocess_strings(string):
    if isinstance(string, str):
        string = string.lower()

        words = nltk.word_tokenize(string)

        words = [word for word in words if word not in stopwords.words("english")]

        stemmer = SnowballStemmer(language="english")

        stemmed_words = [stemmer.stem(word) for word in words]
        stemmed_string = " ".join(stemmed_words)

        return stemmed_string

    return string


def create_soup(
    row,
    keywords_weight=2,
    genres_weight=1,
    cast_weight=2,
    director_weight=2,
    tagline_weight=1,
    overview_weight=1,
):
    soup_parts = ""

    if isinstance(row["keywords"], str):
        soup_parts += (row["keywords"] + " ") * keywords_weight

    if isinstance(row["genres"], str):
        soup_parts += (row["genres"] + " ") * genres_weight

    if isinstance(row["cast"], str):
        soup_parts += (row["cast"] + " ") * cast_weight

    if isinstance(row["director"], str):
        soup_parts += (row["director"] + " ") * director_weight

    if isinstance(row["tagline"], str):
        soup_parts += (row["tagline"] + " ") * tagline_weight

    if isinstance(row["overview"], str):
        soup_parts += (row["overview"] + " ") * overview_weight

    return soup_parts.strip()


def crop_and_merge_data(meta, keywords, credits, soup, min_year=2000):

    meta = pd.DataFrame(meta.loc[meta["release_year"] > min_year])
    meta["release_year"] = meta["release_year"].fillna(0).astype(int)
    for i, row in meta.iterrows():
        meta.at[i, "revised_title"] = f"{row['title']} ({row['release_year']})"

    keywords = keywords[keywords["id"].isin(meta["id"])]
    credits = credits[credits["id"].isin(meta["id"])]
    soup = soup[soup["id"].isin(meta["id"])]

    cropped_data = meta
    cropped_data = pd.merge(cropped_data, keywords, on="id", how="inner")
    cropped_data = pd.merge(cropped_data, credits, on="id", how="inner")

    return cropped_data, soup


def get_top_n_recomm_idx(cosine_sim, n=500):
    top_recommendations = {}

    for idx, row in enumerate(cosine_sim):
        top_indices = np.argsort(row)[::-1][:n]
        top_recommendations[idx] = top_indices.tolist()
    return top_recommendations


def get_poster(movie_id):
    API_KEY = "TMDB AI KEY XYZ"
    url = "https://api.themoviedb.org/3/movie/{}?api_key={}=en-US".format(
        movie_id, API_KEY
    )
    data = requests.get(url)
    data = data.json()

    if "poster_path" in data and data["poster_path"]:
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/original" + poster_path
        return full_path
    else:
        return None
