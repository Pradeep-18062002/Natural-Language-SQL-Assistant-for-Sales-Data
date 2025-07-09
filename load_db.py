import pandas as pd
from sqlalchemy import create_engine
import os

conn_str = os.getenv("DATABASE_URL")
engine = create_engine(conn_str)

df = pd.read_csv("./Sales Data.csv")

df.to_sql("sales",engine,if_exists="replace", index=False)

print("Database Created")