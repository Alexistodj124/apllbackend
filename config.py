#from dotenv import load_dotenv
import os

#load_dotenv()

#local
#user = 'postgres'
#Server
user = 'postgres'
password = 'Alexis2012'
host = 'localhost'
port = '5432'
database = 'taller'

DATABASE_CONNECTION_URI = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)