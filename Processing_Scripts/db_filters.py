"""
Generates filters and filter categories.
Specifically, floating quantity "popularity" is converted to categorical data.
Moreover, TMDB API is used to convert the ISO coded quantities to the full languages and country names.
"""

import pandas as pd
import requests
import ast

headers = {
    "accept": "application/json",
    "Authorization": "[THE AUTHORIZATION TOKEN XYZ]",
}
url_languages = "https://api.themoviedb.org/3/configuration/languages"
url_countries = "https://api.themoviedb.org/3/configuration/countries?language=en-US"


df = pd.read_csv("../Filtered_Data/cropped_full.csv", low_memory=True)

df_filter = df[
    [
        "id",
        "adult",
        "genres",
        "original_language",
        "popularity",
        "production_countries",
        "release_year",
        "vote_average",
    ]
]

percentiles = [0, 0.25, 0.50, 0.75, 1.0]
labels = ["Low", "Medium", "High", "Very High"]

df_filter["popularity_category"] = pd.qcut(
    df_filter["popularity"], q=percentiles, labels=labels
)

df_filter.drop(columns=["popularity"], inplace=True)


def map_iso_to_name(country_list):
    return [iso_to_name_countries[code] for code in ast.literal_eval(country_list)]


response_languages = requests.get(url_languages, headers=headers)
response_languages = response_languages.json()
iso_to_name_languages = {
    item["iso_639_1"]: item["english_name"] for item in response_languages
}
df["original_language"] = df["original_language"].map(iso_to_name_languages)

response_countries = requests.get(url_countries, headers=headers)
response_countries = response_countries.json()
iso_to_name_countries = {
    item["iso_3166_1"]: item["english_name"] for item in response_countries
}
df["production_countries"] = df["production_countries"].apply(map_iso_to_name)


df_filter.to_csv("../Filtered_Data/db_filters.csv", index=False)
