import requests
import os
from urllib.parse import urlparse

def download_file(url, local_path):
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded successfully to {local_path}")
    else:
        print(f"Failed to download. Status code: {response.status_code}")

def create_folder(folder_path):

    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If not, create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def extract_github_slug(github_url):

    # Parse the GitHub URL
    parsed_url = urlparse(github_url)
    # print(parsed_url)
    # Extract the path from the parsed URL
    path_segments = parsed_url.path.split('/')
    # print(path_segments)
    # Check if the path has enough segments to represent a GitHub repository
    if len(path_segments) > 2:
        # Extract the username and repository from the path
        username = path_segments[1]
        repository = path_segments[2]
        
        # Return the GitHub repository slug
        return f"{username}/{repository}"
    else:
        # Return None if the URL doesn't match the expected pattern
        return None
