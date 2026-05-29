import pandas as pd
import os
import boto3
import awswrangler as wr
from dotenv import load_dotenv

load_dotenv() # instantiate => calling load_dotenv()



access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('REGION')

session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

bucket = 'sentinel-landing-1'

data_source = {
    'billing': './extractor/billing.csv'
}

for name, path in data_source.items():
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%d/%m/%Y').dt.date
        wr.s3.to_parquet(
        df=df,
        path=f"s3://{bucket}/source={name}/",
        mode='overwrite',
        dataset=True,
        partition_cols=['transaction_date'],
        boto3_session=session
    )
    else:
        print(f"File {path} does not exist.")