import requests
import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from dotenv import load_dotenv
import os


load_dotenv()


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return value


class JobicyAPI:
    def __init__(self, base_url: str, industry: str, count: int) -> None:
        self.base_url = base_url
        self.industry = industry
        self.count = count
        self.data = None


    def fetch_data(self) -> None:
        url = f"{self.base_url}?count={self.count}&industry={self.industry}"
        response = requests.get(url)

        if response.status_code == 200:
            self.data = response.json()
        
        else:
            response.raise_for_status()
    

    def get_jobs_data(self) -> pd.DataFrame:
        if self.data and 'jobs' in self.data:
            return pd.DataFrame(self.data['jobs'])
        
        else:
            return pd.DataFrame()


class Snowflake:
    def __init__(self, account: str, user: str, password: str, database: str, schema: str, warehouse: str):
        self.engine = create_engine(URL(
            account = account,
            user = user,
            password = password,
            database = database,
            schema = schema,
            warehouse = warehouse,
        ))

    
    def save_to_snowflake(self, df: pd.DataFrame, table_name: str) :
        df.to_sql(table_name, self.engine, if_exists= 'replace', index=False)
        

def main() -> None:
    api = JobicyAPI(
        base_url= "https://jobicy.com/api/v2/remote-jobs",
        industry= "dev",
        count= 10
    )

    api.fetch_data()

    jobs_df = api.get_jobs_data()

    if not jobs_df.empty:
        
        saver = Snowflake(
            account= get_env('ACCOUNT'),
            user= get_env('USER'),
            password= get_env('PASSWORD'),
            database= get_env('DATABASE'),
            schema= get_env('SCHEMA'),
            warehouse= get_env('WAREHOUSE'),
        )

        saver.save_to_snowflake(jobs_df, table_name='remote_works')
        print('Data successfully saved on Snowflake')
    
    else:
        print('There is no data to be saved on Snowflake')

if __name__ == '__main__':
    main()