from flask import Flask, render_template, request
import sys
import os
import pandas as pd
from dotenv import load_dotenv
import re

app = Flask(__name__)

current_directory = os.getcwd()
env_path = os.path.join(current_directory, ".env")
# setting up the env_path variable in the .env file
if os.path.exists(env_path):
    with open(env_path, "r") as env_file:
        lines = env_file.readlines()
        if any(line.startswith(f"PROJECT_DIR={current_directory}") for line in lines):
            print("PROJECT_DIR is already set to the current directory.")
        elif any(line.startswith("PROJECT_DIR=") for line in lines):
            print("PROJECT_DIR exists but points to a different directory.")
        else:
            with open(env_path, "a") as env_file:
                env_file.write(f"\nPROJECT_DIR='{current_directory}'\n")
                print("PROJECT_DIR added to .env")
else:
    with open(env_path, "w") as env_file:
        env_file.write(f"PROJECT_DIR='{current_directory}'\n")
        print(".env file created and PROJECT_DIR added")

load_dotenv()

dir = os.getenv("PROJECT_DIR")

features_dir = os.path.join(dir, "Features")
if features_dir not in sys.path:
    sys.path.append(features_dir)

import Data

dataset = Data.main()

def get_movie_row(movie_name):
    filtered_data = dataset[
        dataset["movie_title"].str.strip().str.match(movie_name, case=False, na=False)
    ]
    return filtered_data

def create_detail_object(filtered_data):
    data = {}
    data["name"] = filtered_data.iloc[0]["movie_title"].title()
    data["director"] = filtered_data.iloc[0]["director_name"]
    data["actors"] = [
        actor
        for actor in [
            filtered_data.iloc[0]["actor_1_name"],
            filtered_data.iloc[0]["actor_2_name"],
            filtered_data.iloc[0]["actor_3_name"],
        ]
        if actor.lower() != "unknown"
    ]
    data["genres"] = filtered_data.iloc[0]["genres"].split(" ")
    data["reviews"] = filtered_data.iloc[0]["imdb_reviews"]
    data["poster"] = filtered_data.iloc[0]["poster_url"]
    data["description"] = filtered_data.iloc[0]["description"].capitalize()
    return data

@app.route("/recommend", methods=["GET"])
def recommend(search=None):
    # if search:
    #     filtered_data = dataset[
    #         dataset["movie_title"].str.contains(search, case=False, na=False)
    #     ]
    #     if not filtered_data.empty:
    #         data = filtered_data.to_dict(orient="records")
    # else:
    movie_name = "the sonata"
    filtered_data = get_movie_row(movie_name)
    print("hello", filtered_data.iloc[0]["genres"])
    if not filtered_data.empty:
        data = create_detail_object(filtered_data)
        return render_template("recommend.html", data=data)
    else:
        return render_template("error.html")
        


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port="5000")
