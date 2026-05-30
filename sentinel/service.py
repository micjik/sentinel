import os
import glob
import json
import boto3
import pandas as pd
import awswrangler as wr
from dotenv import load_dotenv

load_dotenv()
access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('REGION')

bucket = 'sentinel-processed-1'

session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)

for day_folder in os.listdir('./output_dir'):
    day_path = f'./output_dir/{day_folder}'

    if not os.path.isdir(day_path):
        continue

    json_files = glob.glob(f'{day_path}/*.json')

    if not json_files:
        continue

    dfs = []
    expected_columns = ['claim_id', 'policy_id', 'claim_amount', 'claim_date', 'claim_status', 'source']
    for f in json_files:
        with open(f) as file:
            data = json.load(file)
            # Handle both single object and array
            df = pd.json_normalize(data if isinstance(data, list) else [data])
            dfs.append(df)

    day_df = pd.concat(dfs, ignore_index=True)
    day_value = day_folder.split('=')[-1]

    wr.s3.to_parquet(
        df=day_df,
        path=f"s3://{bucket}/output_dir/day={day_value}/claims_mgmt/",
        mode='overwrite',
        dataset=True,
        boto3_session=session
    )

    