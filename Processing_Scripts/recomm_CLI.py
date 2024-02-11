"""
A simple Command Line Interface based application to check the functioning of recommender.
"""

import pickle
import pandas as pd

with open("../Model/top_recomm_idx.pkl", "rb") as f:
    top_recomm_idx = pickle.load(f)

title_id = pd.read_csv("../Filtered_Data/cropped_title_id.csv", low_memory=True)


def get_recommendations(title, recomm_dict, df_title, n=10):
    try:
        idx = df_title[df_title["revised_title"] == title].index[0]
        top_indices = recomm_dict[idx][1 : n + 1]
        recommended_titles = df_title.iloc[top_indices]["revised_title"].values

        print(f"\nTop {n} recommendations for '{title}':")
        for i, recommended_title in enumerate(recommended_titles, 1):
            print(f"{i}. {recommended_title}")
    except IndexError:
        print(f"Title '{title}' not found in the DataFrame.")


while True:
    sample_titles = title_id["revised_title"].sample(5)

    print("\nSample of 5 Titles:")
    for idx, title in enumerate(sample_titles, 1):
        print(f"{idx}. {title}")

    title = input(
        "\nEnter Movie Name to get recommendations (Press Enter for new titles): "
    )

    if not title:
        continue
    else:
        break


get_recommendations(title, top_recomm_idx, title_id, n=10)
