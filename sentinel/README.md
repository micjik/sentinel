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
- ``


### My Process
 - `policy admin extractor connect to the PostgreSQL database and`
   `pulls customers, agents, policies and coverage data from the database to amazon simple storage system`



### SERVICES


### Other Developers
