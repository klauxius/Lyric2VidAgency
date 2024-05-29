from agency_swarm.tools import BaseTool
from pydantic import Field
import requests
import time
from urllib.parse import urlparse
from selenium.common import WebDriverException
from browsing.util.selenium import get_web_driver, set_web_driver
from browsing.util import get_web_driver, set_web_driver, get_b64_screenshot
from browsing.util.highlights import highlight_elements_with_labels, remove_highlight_and_labels
from agency_swarm.util import get_openai_client
from selenium.webdriver.common.by import By
from typing import Literal
import base64
import json
from firecrawl import FirecrawlApp
import os
import dotenv
dotenv.load_dotenv()
app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))




class getGeniusurl(BaseTool):
    """This tool uses the Genius API to find the URL of the webpage containing the lyrics. This should be the first tools used to in the lyricist's workflow."""
    url: str = Field(
        ..., description="Url to Genius webpage to find lyrics."
    )

    Search: str = Field(
        ..., description="The search term used to find the song."
    )

    def run(self):
        # Enter your tool code here. It should return a string.
        # Function to search for the song ID
        def search_song(api_token, search_term):
            api_url = f"https://api.genius.com/search?q={search_term}"
            headers = {'Authorization': f'Bearer {api_token}'}
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return response.json()['response']['hits'][0]['result']['id']
            else:
                return None
        # Function to get song data including the lyrics URL

        # Gets the song url    
        def get_song_data(api_token, song_id):
            api_url = f"https://api.genius.com/songs/{song_id}"
            headers = {'Authorization': f'Bearer {api_token}'}
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return response.json()['response']['song']['url']  # The URL of the song's Genius page
            else:
                return None

        #Uses the url to get the webpage for the lyrics    
        api_token = os.getenv("GENIUS_API_KEY")  # Replace with your actual API token
        search_term = self.Search
        song_id = search_song(api_token, search_term)
        url = get_song_data(api_token, song_id)
        # do_something(self.url)

        return url
    
    
class AnalyzeContent(BaseTool):
    """
    This tool analyzes the current web browser window content and returns a scaped markdown file of the content on the webpage. This should be used after the get genius url tool to analyze the content of the webpage."""
    lyrics_url: str = Field(
        ..., description="URL of the webpage to analyze."
    )
    
    def run(self):
        

        response = app.scrape_url(url=self.lyrics_url)


        return response
    
class SaveLyrics(BaseTool):
    """
    This tool saves the lyrics text found on the genius webpage as JSON file in the file directory.
    """
    lyrics: str = Field(
        ..., description="Lyrics text to save as a JSON file."
    )
    filepath: str = Field(
        ..., description="Filepath to save the JSON file."
    )

    def run(self):
        data = {
            "lyrics": self.lyrics
        }

        with open(self.filepath, "w") as file:
            json.dump(data, file)

        return "Lyrics saved as JSON file."

