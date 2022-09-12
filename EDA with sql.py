%load_ext sql

import csv, sqlite3

con = sqlite3.connect("my_data1.db")

cur = con.cursor()

!pip install -q pandas==1.1.5

%sql sqlite:///my_data1.db
  
import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")


%%sql
SELECT DISTINCT(Launch_Site) FROM SPACEXTBL


%%sql
SELECT * FROM SPACEXTBL
    WHERE Launch_Site Like 'CCA%'
    LIMIT 5
    
%%sql
SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL
    WHERE Customer = 'NASA (CRS)'
  

%%sql
SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL
    WHERE Booster_Version LIKE 'F9 v1.1%' 


%%sql
SELECT MIN(substr(Date,7,4) || substr(Date,4,2) || substr(Date,1,2)) AS DATE FROM SPACEXTBL
    WHERE [Landing _Outcome] = 'Success (ground pad)'


%%sql
SELECT DISTINCT(Booster_Version) FROM SPACEXTBL
    WHERE [Landing _Outcome] = 'Success (drone ship)'
    AND ([PAYLOAD_MASS__KG_] BETWEEN 4000 AND 6000)


%%sql
SELECT [Landing _Outcome], COUNT ([Landing _Outcome]) FROM SPACEXTBL
    GROUP BY [Landing _Outcome]
  

%%sql
SELECT DISTINCT(Booster_Version) FROM SPACEXTBL
    WHERE [PAYLOAD_MASS__KG_] IN (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)
  

%%sql
SELECT SUBSTR(DATE, 4, 2) AS Month, [Landing _Outcome], [Booster_Version], [Launch_Site] FROM SPACEXTBL
    WHERE [Landing _Outcome] = 'Failure (drone ship)' AND SUBSTR(Date, 7, 4) = '2015'
  
  
%%sql
SELECT DATE, [Landing _Outcome], COUNT([Landing _Outcome]) FROM SPACEXTBL
    WHERE [Landing _Outcome] LIKE 'Success%' AND (SUBSTR(DATE, 7, 4) || SUBSTR(DATE, 4,2) || SUBSTR(DATE, 1, 2)) BETWEEN '20100604' AND '20170312'
    GROUP BY [Landing _Outcome]
    ORDER BY 'LANDING _Outcome' DESC
