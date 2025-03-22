import json
import Data

def Collaborative(movie_row):
    dataset = Data.main()
    
    movie_name = movie_row.get("movie_title", "")
    director = movie_row.get("director_name", "").split(", ") if movie_row.get("director_name") else []
    actors = [
        movie_row.get("actor_1_name", ""),
        movie_row.get("actor_2_name", ""),
        movie_row.get("actor_3_name", "")
    ]
    genres = movie_row.get("genres", "").split(" ") if movie_row.get("genres") else []

    weights = {"director": 0.15, "actors": 0.25, "genres": 0.6}
    similarity_scores = {}

    for row in dataset:
        if row.get("movie_title") == movie_name:
            continue

        iterated_director = row.get("director_name", "").split(", ") if row.get("director_name") else []
        iterated_actors = [
            row.get("actor_1_name", ""),
            row.get("actor_2_name", ""),
            row.get("actor_3_name", "")
        ]
        iterated_genres = row.get("genres", "").split(" ") if row.get("genres") else []

        director_similarity = (
            len(set(director).intersection(iterated_director)) /
            max(1, len(set(director).union(iterated_director))) * weights["director"]
        )
        actor_similarity = (
            len(set(actors).intersection(iterated_actors)) /
            max(1, len(set(actors).union(iterated_actors))) * weights["actors"]
        )
        genre_similarity = (
            len(set(genres).intersection(iterated_genres)) /
            max(1, len(set(genres).union(iterated_genres))) * weights["genres"]
        )

        total_similarity = director_similarity + actor_similarity + genre_similarity
        similarity_scores[row["movie_title"]] = total_similarity

    top_10_movies = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:10]

    top_10_movies_poster_json = json.dumps(
        {movie.title(): next((item["poster_url"] for item in dataset if item["movie_title"] == movie), "")
         for movie, _ in top_10_movies},
        indent=4
    )

    return top_10_movies_poster_json

if __name__ == "__main__":
    Collaborative()