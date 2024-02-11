"""
Handles all necessary and final preprocessing required and prepares the data to be passed on to the Vectorizer model.
Create a mixture of all textual data useful for recommending movies such as cast, director, keywords, tagline, etc.
"""

import warnings

warnings.filterwarnings("ignore")
import pandas as pd
import ast
import re
from process_utils import *

df_meta = pd.read_csv("../Clean_Data/clean_metadata.csv", low_memory=True)
df_keywords = pd.read_csv("../Clean_Data/clean_keywords.csv", low_memory=True)
df_credits = pd.read_csv("../Clean_Data/clean_credits.csv", low_memory=True)

filtered_df = df_meta[["id", "genres", "overview", "tagline"]]
filtered_df = pd.merge(filtered_df, df_keywords, on="id", how="inner")
filtered_df = pd.merge(filtered_df, df_credits, on="id", how="inner")
filtered_df = filtered_df.filter(regex=r"^(?!Unnamed)")
filtered_df.rename(columns={"crew": "director"}, inplace=True)

filtered_df["director"] = filtered_df["director"].apply(
    lambda x: process_list_elements(ast.literal_eval(x))
)
filtered_df["cast"] = filtered_df["cast"].apply(
    lambda x: process_list_elements(ast.literal_eval(x))
)
filtered_df["genres"] = filtered_df["genres"].apply(
    lambda x: process_list_elements(ast.literal_eval(x))
)
filtered_df["keywords"] = filtered_df["keywords"].apply(
    lambda x: process_list_elements(ast.literal_eval(x))
)

for index, row in filtered_df.iterrows():
    if isinstance(row["director"], list):
        filtered_df.at[index, "director"] = row["director"][:3]

filtered_df["director"] = filtered_df["director"].apply(lambda x: " ".join(x))
filtered_df["cast"] = filtered_df["cast"].apply(lambda x: " ".join(x))
filtered_df["genres"] = filtered_df["genres"].apply(lambda x: " ".join(x))
filtered_df["keywords"] = filtered_df["keywords"].apply(lambda x: " ".join(x))

filtered_df["overview"] = filtered_df["overview"].apply(preprocess_strings)
filtered_df["tagline"] = filtered_df["tagline"].apply(preprocess_strings)

for i, row in filtered_df.iterrows():
    filtered_df.at[i, "soup"] = create_soup(row=row)

filtered_df[["id", "soup"]].to_csv("../Filtered_Data/soup.csv", index=False)
