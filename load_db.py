import pandas as pd
from sqlalchemy import create_engine

conn_str = "postgresql://neondb_owner:npg_7tGicxTqN6rm@ep-icy-bar-ae2i4okh-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(conn_str)

df = pd.read_csv("./Sales Data.csv")

df.to_sql("sales",engine,if_exists="replace", index=False)

print("Database Created")