import psycopg2
import pandas as pd
import os
import boto3
import awswrangler as wr
from dotenv import load_dotenv
from datetime import date

load_dotenv() # instantiate => calling load_dotenv()



access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('REGION')
password = os.getenv("your_password")



today = date.today().strftime("%Y-%m-%d")


# Connect to the postgres database
conn = psycopg2.connect(
    database="PublicAdmin",
    user="postgres",
    password= password,
    host="localhost",
    port="5432"
    
)

customers = pd.read_sql("SELECT * FROM customers", conn)
agents = pd.read_sql("SELECT * FROM agents", conn)
coverages = pd.read_sql("SELECT * FROM coverages", conn)
policies = pd.read_sql("SELECT * FROM policies", conn)

print("connection successful")

conn.close()

bucket = 'sentinel-landing-1'

#Create a Session
session = boto3.Session(
    aws_access_key_id= access_key,
    aws_secret_access_key= secret_key,
    region_name= region
)

data_source = {
    'customers':customers,
    'agents':agents,
    'coverages':coverages,
    'policies' :policies
}

for name, df in data_source.items():
        wr.s3.to_parquet(
            df = df,
            path = f"s3://{bucket}/source=policy_admin/table={name}/day={today}/{name}.parquet",
            index = False,
            mode = 'overwrite',
            dataset = True,
            boto3_session = session
        )
        
    
        


#QUERY = "SELECT * FROM customers"
#df = pd.read_sql(QUERY, conn)

#cur = conn.cursor()
#conn.close()