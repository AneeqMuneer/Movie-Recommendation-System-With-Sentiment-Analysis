import csv
import ast
import os
from dotenv import load_dotenv

load_dotenv()

dir = os.getenv("PROJECT_DIR")

def read_csv(file_path):
    """Reads a CSV file and returns a list of dictionaries."""
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def combine_csvs():
    """Combines multiple CSV datasets into a single list of dictionaries."""
    data_2016 = read_csv(f"{dir}/Dataset/data_2016.csv")
    data_2018 = read_csv(f"{dir}/Dataset/data_2018.csv")
    data_2019 = read_csv(f"{dir}/Dataset/data_2019.csv")
    data_2020 = read_csv(f"{dir}/Dataset/data_2020.csv")
    return data_2016 + data_2018 + data_2019 + data_2020

def parse_reviews(review_str):
    """Parses a string representation of a list of reviews into an actual list."""
    try:
        reviews = ast.literal_eval(review_str)
        if isinstance(reviews, list):
            return [review.strip() for review in reviews]
        else:
            return []
    except (ValueError, SyntaxError):
        return []

def process_reviews(data):
    """Processes review data in each row to ensure it is stored as a list."""
    for row in data:
        if "imdb_reviews" in row:
            row["imdb_reviews"] = parse_reviews(row["imdb_reviews"])
    return data

def main():
    """Returns processed data as a list of JSON objects."""
    combined_data = combine_csvs()
    processed_data = process_reviews(combined_data)
    return processed_data  # No file saving, just returning the list

if __name__ == "__main__":
    processed_data = main()
    print(processed_data[:2])  # Print first two items for preview