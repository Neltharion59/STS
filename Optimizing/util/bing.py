import requests

import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)
from util.file_handling import read

token_path = os.path.join(root_path, 'resources', 'tokens', 'bing.txt')
token = read(token_path)
url = "https://api.bing.microsoft.com/v7.0/search"


def search_result_count(search_query, tries=10):
    # Headers with API key
    headers = {"Ocp-Apim-Subscription-Key": token}

    # Parameters with the query
    params = {"q": search_query}

    for i in range(tries):
        try:
            # Send the GET request
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                # Extract the total number of estimated results
                return data.get("webPages", {}).get("totalEstimatedMatches", 0)
        except Exception:
            pass

    print(f"Error: {response.status_code}, {response.text}")
    return -1
