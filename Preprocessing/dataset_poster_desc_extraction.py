import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import html
import sys
import os

sys.path.append(os.path.abspath('../Features'))

import Data

output_file = '../Dataset/alldata.csv'
df = Data.main()

if 'imdb_url' not in df.columns:
    raise ValueError("The DataFrame must contain an 'imdb_url' column.")

df['poster_url'] = ''
df['description'] = ''

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

for index, row in df.iterrows():
    imdb_url = row['imdb_url']

  
    cleaned_url = imdb_url.split('/?')[0]

  
    response = requests.get(cleaned_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

      
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            try:
                raw_json = script_tag.string.strip()
                movie_data = json.loads(raw_json)

              
                poster_url = movie_data.get('image', 'No poster URL available')
                description = movie_data.get('description', 'No description available')
                decoded_description = html.unescape(description)

              
                df.at[index, 'poster_url'] = poster_url
                df.at[index, 'description'] = decoded_description
                print("Added poster and description for movie")
            except json.JSONDecodeError:
                print(f"Failed to decode JSON for URL: {cleaned_url}")
        else:
            print(f"JSON data not found for URL: {cleaned_url}")
    else:
        print(f"Failed to fetch data for URL: {cleaned_url}. Status code: {response.status_code}")

df.to_csv(output_file, index=False)
print(f"Data successfully saved to {output_file}")