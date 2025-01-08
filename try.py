from flask import Flask, render_template, request
import sys
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

dir = os.getenv("PROJECT_DIR")

features_dir = os.path.join(dir, "Features")
if features_dir not in sys.path:
    sys.path.append(features_dir)

import Data

dataset = Data.main()

data = {}
filtered_data = dataset[
    dataset["movie_title"].str.match("the sonata", case=False, na=False)
]
if not filtered_data.empty:
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

print(data["name"])
print(data["director"])
print("Actors:")
for actor in data["actors"]:
    print(actor)
print("Genres:")
for genre in data['genres']:
    print(genre)
print("First Review:")
if isinstance(data["reviews"], list) and data["reviews"]:
    print(data["reviews"][0])
print(data["poster"])
print(data["description"])