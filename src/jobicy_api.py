import requests
import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv
import os


class JobicyAPI:
    def __init__(self, base_url: str, industry: str, count: int) -> None:
        self.base_url = base_url
        self.industry = industry
        self.count = count
        self.data = None


    def fetch_data(self) -> None:
        url = f"{self.base_url}?count={self.count}&{self.industry}"
        response = requests.get(url)

        if response.status_code == 200:
            self.data = response.json()
        
        else:
            response.raise_for_status()