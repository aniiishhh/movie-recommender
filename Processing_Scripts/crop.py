"""
Crops the dataset and reduces the size by almost 50% to simplify the app production.
Extracts all movies whose release data is after 2000.
"""

import pandas as pd
from process_utils import crop_and_merge_data

meta = pd.read_csv("./Clean_Data/clean_metadata.csv", low_memory=True)
keywords = pd.read_csv("./Clean_Data/clean_keywords.csv", low_memory=True)
credits = pd.read_csv("./Clean_Data/clean_credits.csv", low_memory=True)
soup = pd.read_csv("./Filtered_Data/soup.csv", low_memory=True)

cropped_data, cropped_soup = crop_and_merge_data(
    meta, keywords, credits, soup, min_year=2000
)

cropped_data = cropped_data.filter(regex=r"^(?!Unnamed)")
cropped_data.drop(columns=["keywords_str"], inplace=True)

cropped_title_id = cropped_data[["id", "revised_title"]]

cropped_data.to_csv("./Filtered_Data/cropped_full.csv", index=False)
cropped_soup.to_csv("./Filtered_Data/cropped_soup.csv", index=False)
cropped_title_id.to_csv("./Filtered_Data/cropped_title_id.csv", index=False)
