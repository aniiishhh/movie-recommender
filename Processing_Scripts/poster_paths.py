"""
Extracts the movie poster paths using TMDB API and saves it in the database.
Helper function (get_poster) implementation defined in ./process_utils.py
"""

import pandas as pd
from process_utils import get_poster

df = pd.read_csv("../Filtered_Data/cropped_full.csv", low_memory=True)

for i, row in df.iterrows():
    df.at[i, "poster_path"] = get_poster(row["id"])

df.to_csv("../Filtered_Data/cropped_full.csv", index=False)
