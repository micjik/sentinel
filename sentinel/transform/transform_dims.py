import pandas as pd
import os
import boto3
import awswrangler as wr
from dotenv import load_dotenv

load_dotenv() # instantiate => calling load_dotenv()

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('REGION')



bucket = 'sentinel-landing-1'

session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
)

dfs ={}

policy_admin_tables = ["customers", "agents", "coverages", "policies"]
dfs["policy_admin"] = {}

for name in policy_admin_tables:
    dfs["policy_admin"][name] = wr.s3.read_parquet(
        path=f"s3://{bucket}/source=policy_admin/table={name}/",
        dataset=False,
        boto3_session=session
    )

    print(f"Shape: {dfs['policy_admin'][name].head}")
print(f"Nulls:\n{dfs['policy_admin'][name].isnull().sum()}")

df_weather = wr.s3.read_parquet(
    path=f"s3://{bucket}/source=weather/",
    dataset=True,
    boto3_session=session
)

# check for duplicate rows with primary id
primary_keys = {
    "customers": "customer_id",
    "agents": "agent_id",
    "coverages": "coverage_id",
    "policies": "policy_id"
}

for name, pk in primary_keys.items():
    df = dfs["policy_admin"][name]
    dupes = df[df.duplicated(subset=[pk], keep=False)]
    data_types = df.info()

    print(df.columns.tolist())

date_cols_customers = ['dob']
for col in date_cols_customers:
    dfs["policy_admin"]["customers"][col] = pd.to_datetime(dfs["policy_admin"]["customers"][col]).dt.date

# agents
dfs["policy_admin"]["agents"]["hire_date"] = pd.to_datetime(dfs["policy_admin"]["agents"]["hire_date"]).dt.date

# policies
date_cols_policies = ['start_date', 'end_date']
for col in date_cols_policies:
    dfs["policy_admin"]["policies"][col] = pd.to_datetime(dfs["policy_admin"]["policies"][col]).dt.date


print(dfs["policy_admin"]["customers"]['dob'].dtype)
print(dfs["policy_admin"]["agents"]['hire_date'].dtype)
print(dfs["policy_admin"]["policies"]['start_date'].dtype)
print(dfs["policy_admin"]["policies"]['end_date'].dtype)
print(type(dfs["policy_admin"]["customers"]['dob'].iloc[0]))
    #df['hire_date'] = pd.to_datetime(df['hire_date']).dt.date
    #df['end_date'] = pd.to_datetime(df['end_date']).dt.date
   # if not dupes.empty:
    #    print(f"[{name}] {len(dupes)} duplicate rows on '{pk}':")
     #   print(dupes[pk].value_counts())

# check data types and convert money field to decimal(18,2)

cleaned_bucket = 'sentinel-processed-1'

#for name in policy_admin_tables:
#    wr.s3.to_parquet(
 #       df=dfs["policy_admin"][name],
 #       path=f"s3://{cleaned_bucket}/source=policy_admin/table={name}/{name}.parquet",
  #      dataset=False,
   #     boto3_session=session
    #)
   # print(f"Written: {name} -> s3://{cleaned_bucket}/source=policy_admin/table={name}/")

wr.s3.to_parquet(
         df=df_weather,
         path=f"s3://{cleaned_bucket}/source=weather/",
         dataset=True,
         mode='overwrite',
         partition_cols=['weather_date'],
         boto3_session=session
)
