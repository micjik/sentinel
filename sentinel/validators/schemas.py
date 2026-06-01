import pandas as pd
import os
import boto3
import awswrangler as wr
from dotenv import load_dotenv

load_dotenv() # instantiate => calling load_dotenv()

access_key = os.getenv('ACCESS_KEY')
secret_key = os.getenv('SECRET_KEY')
region = os.getenv('REGION')

print(f"Access Key: {access_key}")
print(f"Secret Key: {secret_key}")
print(f"Region: {region}")  

try:
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    sts = session.client("sts")
    identity = sts.get_caller_identity()
    print(f"Connected as: {identity['Arn']}")
except Exception as e:
    print(f"Error: {e}")

bucket = 'sentinel-landing-1'

sources = ["billing",  "weather"]

dfs = {}
for source in sources:
    dfs[source] = wr.s3.read_parquet(
        path=f"s3://{bucket}/source={source}/",
        dataset=True,
        boto3_session=session
    )

policy_admin_tables = ["customers", "agents", "coverages", "policies"]
dfs["policy_admin"] = {}  


for name in policy_admin_tables:
    dfs["policy_admin"][name] = wr.s3.read_parquet(
        path=f"s3://{bucket}/source=policy_admin/table={name}/",
        dataset=False,
        boto3_session=session
    )
# access each one like this
#print(dfs["billing"].head())
# transaction_id  policy_id customer_id transaction_type   amount payment_method  status   source  transaction_date
# string           string    string      string           float64  string          string   category category
#print(dfs["weather"].head())
# zip_code          city state  precipitation_mm  max_wind_kmh  ...  min_temp_c  weather_code  severity       source   weather_date
# Int64             string  string  float64           float64       ...  float64      Int64      string     category  category

print(dfs["billing"].dtypes)
print(dfs["weather"].dtypes)

df_billing = dfs["billing"]

# extract rows where payment_method is null
null_payment = df_billing[df_billing['payment_method'].isnull()]
clean_billing = print(df_billing[df_billing['payment_method'].notnull()])

print(f"Clean rows: {len(clean_billing)}")
print(f"Null rows: {len(null_payment)}")

# send null rows to quarantine
if len(null_payment) > 0:
    wr.s3.to_parquet(
        df=null_payment,
        path=f"s3://{bucket}/source=billing/quarantine/null_payment_method.parquet",
        dataset=False,
        boto3_session=session
    )
    print(f"Moved {len(null_payment)} null rows to quarantine")

   # step 1 - delete old billing files
wr.s3.delete_objects(
    path=f"s3://{bucket}/source=billing/",
    boto3_session=session
)

# step 2 - ensure consistent type before upload
#df['transaction_date'] = pd.to_datetime(df['transaction_date'], format='%d/%m/%Y').dt.date.astype(str)

# step 3 - re-upload cleanly
#wr.s3.to_parquet(
#    df=df,
 #   path=f"s3://{bucket}/source=billing/",
 #   dataset=True,
 #   mode='overwrite',
 #   boto3_session=session
#)

#print(dfs["billing"].isnull().sum())
#print(dfs["weather"].isnull().sum())
#print(f"\n--- policy_admin/{name} ---")
#(f"Shape: {dfs['policy_admin'][name].shape}")
#print(f"Nulls:\n{dfs['policy_admin'][name].isnull().sum()}")


#print(dfs["policy_admin"].shape)
# drop rows where ALL columns are null
#df = dfs["policy_admin"].dropna(how='all')
#print(df.shape)  # should show reduced row count

#null_rows = dfs["billing"][dfs["billing"]['payment_method'].isnull()]
#print(f"Found {len(null_rows)} null rows")
#print(null_rows.head())

#bucket = 'sentinel-landing-1'
    
