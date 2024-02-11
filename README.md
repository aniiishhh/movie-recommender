****Movie Recommendation App****

---

**Introduction:**

Welcome to the Movie Recommendation App! This application leverages a sophisticated content-based recommendation engine to suggest movies based on user preferences and selected films. With a clean and intuitive interface, users can effortlessly explore a vast collection of movies and discover new favorites.

The dataset used in this application is an extensively filtered and cleaned version of the [Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset) from Kaggle. This dataset serves as the foundation for generating personalized movie recommendations tailored to each user's tastes.

To experience the app firsthand, visit the web app link created with Streamlit: [Movie Recommendation App](https://recommend-movies-ak.streamlit.app/)

---

**Features:**

- **Interactive Recommendations:** Users can explore movie recommendations by selecting a film of their choice and applying various filters such as genres, minimum rating, popularity, release year, countries, and languages.

- **Efficient Data Processing:** The Notebooks folder includes EDA.ipynb, a Jupyter notebook where initial dataset exploration and analysis took place. Additionally, the Processing_Scripts directory contains Python scripts for dataset processing and implementation of the text vectorizer.

- **Streamlined Data Retrieval:** The app optimizes data retrieval from the PostgreSQL database, ensuring fast and efficient access to movie information. 

- **Dynamic Frontend:** Posters and other visual elements enrich the user experience, making movie exploration engaging and visually appealing.

---

**Tech Stack:**

- **Backend:** PostgreSQL database is used for efficient data storage and retrieval.
- **Frontend:** Python, along with Streamlit, powers the frontend interface, providing a seamless and interactive user experience.
- **Data Processing:** Various Python scripts handle data processing tasks, ensuring the dataset is clean and optimized for recommendation generation.
- **API Integration:** The app integrates with the TMDB API to fetch additional movie data and enhance the recommendation process.

---

**Acknowledgments and References:**

1. Dataset Source: [The Movies Dataset](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
2. Frontend and Web App Hosting: [Streamlit](https://streamlit.io/)
3. PostgreSQL Database Hosting: [Render](https://render.com/)

---

Explore the Movie Recommendation App today and discover a world of cinematic possibilities at your fingertips!
