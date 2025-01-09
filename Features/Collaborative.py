# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize

# Assuming `Data.main()` returns the dataset as a pandas DataFrame
import Data

def Collaborative():
    # Load the dataset
    dataset = Data.main()

    # Drop the "imdb-reviews" column
    dataset = dataset.drop(columns=["imdb_url","imdb_reviews","poster_url","description"])

    # Convert all multi-entry columns (e.g., directors, actors, genres) into sets for each movie
    for col in dataset.columns:
        dataset[col] = dataset[col].apply(lambda x: set(x.split(", ")) if isinstance(x, str) else set())

    # Create a co-occurrence matrix
    num_movies = len(dataset)
    co_occurrence_matrix = np.zeros((num_movies, num_movies))

    # Compute co-occurrence
    for i in range(num_movies):
        for j in range(num_movies):
            if i != j:
                # Find the intersection of sets for all columns
                shared_features = sum(
                    len(dataset.iloc[i][col].intersection(dataset.iloc[j][col]))
                    for col in dataset.columns
                )
                co_occurrence_matrix[i, j] = shared_features

    # Normalize the co-occurrence matrix row-wise
    normalized_matrix = normalize(co_occurrence_matrix, norm="l1", axis=1)

    # Save the normalized matrix as a .npy file
    np.save("normalized_co_occurrence_matrix.npy", normalized_matrix)

    print("Normalized co-occurrence matrix saved as 'normalized_co_occurrence_matrix.npy'.")

    return normalized_matrix

if __name__ == "__main__":
    Collaborative()