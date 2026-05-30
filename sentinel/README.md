# Project Name: Sentinel Auto Insurance

## Table of Contents
- `Overview`
- `Challenges`
- `Screenshot`
- `My process`
- `Built with`
- `What I learned`
- `Author`
- `Acknowledgements`

### Overview
this project focuses on integrating sentinel's three operational systems plus one external weather API into one centralized internal data platform and this achieved by first extracting the data from each source and move them into a multi-zone s3 data lake, transform it with pandas and loads it into snowflake dimensional warehouse on a daily schedule.
https://www.geeksforgeeks.org/postgresql/postgresql-connecting-to-the-database-using-python/



### Screen-shot Data Pipeline Architecture
![Data Pipeline Architecture](./myproject/image.png)

### Built with (project Tech Stack and Flow)
- 

### Challenges

- `had couple of issues while connecting my python script to amazon s3 like the permission was not set properly so the accesskey and secret key could not be read `
- `difficulty using the google drive api, so I deployed in using the gdown to download the files from google drive`
- `while trying to read data from s3 to check for null values, I realized in the apolicy_admin, I was having large numbers of nulls in the policy_admin because it has four tables and when checking for null, I did not check null for each table instead I was checking for null in policy_admin and assuming it was a table. Realized it has four tables`


### My Process
 - `policy admin extractor connect to the PostgreSQL database and`
   `pulls customers, agents, policies and coverage data from the database to amazon simple storage system`
 - `use gdown to download the files from google drive`
 - `extract data from weather api and billing.csv to s3
 - `read data from s3 to check for data integrity and consistence`
 - `extract null value to s3 and names it sentinel-landing-1/quarantine`






### SERVICES
https://thepythoncode.com/article/using-google-drive--api-in-python#Download_Files

### Other Developers
