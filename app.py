import streamlit as st
import json
from Classifier import KNearestNeighbours
from operator import itemgetter


# Load data and movies list from corresponding JSON files
with open(r'data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)


def knn(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Distances to most distant movie
    max_dist = sorted(model.distances, key=itemgetter(0))[-1]
    # Print list of 10 recommendations < Change value of k for a different number >
    table = list()
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2]])
    return table


if __name__ == '__main__':
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    st.header('Rekomendasi Film')
    apps = ['--Pilih--', 'Berdasarkan Film', 'Berdasarkan Kriteria']
    app_options = st.selectbox('Pilih Tipe Rekomendasi:', apps)
    if app_options == 'Berdasarkan Film':
        movie_select = st.selectbox('Pilih Film:', ['--Select--'] + movies)
        if movie_select == '--Select--':
            st.write('Pilih Film')
        else:
            n = st.number_input('Banyaknya Film:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(movie_select)]
            test_point = genres
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
    elif app_options == apps[2]:
        options = st.multiselect('Pilih Genre:', genres)
        if options:
            imdb_score = st.slider('IMDb score:', 1, 10, 8)
            n = st.number_input('Banyaknya Film:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in options else 0 for genre in genres]
            test_point.append(imdb_score)
            table = knn(test_point, n)
            for movie, link in table:
                # Displays movie title with link to imdb
                st.markdown(f"[{movie}]({link})")
        else:
            st.write("Ini adalah website rekomendasi film sederhana."
                     "Kamu bisa memilih genre dan mengubah score IMDb sesuai yang kamu mau.")
    else:
        st.write('Pilih Pilihan')
