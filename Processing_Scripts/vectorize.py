"""
Create word vectors for the mixture of textual data prepared in ./preprocess_text.py
Only top 500 recommendations are saved for every movie due to hardware restrictions.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
from process_utils import get_top_n_recomm_idx

soup = pd.read_csv("../Filtered_Data/cropped_soup.csv", low_memory=True)

tf = TfidfVectorizer(analyzer="word", ngram_range=(1, 2), min_df=1)
tf_matrix = tf.fit_transform(soup["soup"])

cosine_sim = linear_kernel(tf_matrix, tf_matrix)

top_recomm_indices = get_top_n_recomm_idx(cosine_sim, n=500)

with open("../Model/top_recomm_idx.pkl", "wb") as file:
    pickle.dump(top_recomm_indices, file)
