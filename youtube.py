# Import necessary modules and libraries
import requests
import json
# Import data processing helper
from helpers import process_results
# Import pandas to create dataframe
import pandas as pd
# Import sys dependency to extract command line argument
import sys
# Import os
import streamlit as st

# Define function to get hashtag dynamically
def get_data(hashtag):

    # Get API key and host from environment variables
    api_key = st.secrets["RAPIDAPI_KEY"]
    api_host = st.secrets["RAPIDAPI_HOST"]
    
    # Define the URL for the API endpoint
    url = "https://yt-api.p.rapidapi.com/hashtag"
    # Define the query parameters for the request
    querystring = {"tag": hashtag}
    # Set the headers, including the API key and host
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    # Send a GET request to the API with the specified URL, headers, and query parameters
    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        full_data = response.json()
        print(full_data)  # Print the full data to check if API is returning expected response
        data = full_data.get('data', [])  # Extract the 'data' part
        flattened_data = process_results(data)

        # Save the JSON data to a file named 'output.json'
        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump(flattened_data, json_file, ensure_ascii=False, indent=4)
    # Check if request failed
    else:
        # Print an error message if the request failed
        print(f"Request failed with status code: {response.status_code}")
        
    # Creating a new dataframe from processed data
    df = pd.DataFrame.from_dict(flattened_data, orient='index')
    # Standardize column names
    col_new_names = ['Video ID','Title','Channel Title','Channel ID','Channel Thumbnail URL','Channel Thumbnail Width','Channel Thumbnail Height','View Count','Published Time Text','Publish Date','Published At','Video Length Text','Thumbnail URL','Thumbnail Width','Thumbnail Height']
    # Check for column value mismatch
    if len(df.columns) == len(col_new_names):
        df.columns = col_new_names
        # Save dataframe to csv file
        df.to_csv('youtubedata.csv', index=False) 
    else:
        # Return a message indicating empty data
        print("No data to process")
        return False

if __name__ == '__main__':
    # Check if a hashtag argument is passed
    if len(sys.argv) < 2:
        print("Error: No hashtag provided. Please provide a hashtag to search.")
        sys.exit(1)
    
    get_data(sys.argv[1])
