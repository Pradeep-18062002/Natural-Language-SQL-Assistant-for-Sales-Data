from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text 
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
engine = create_engine(DATABASE_URL)

app = FastAPI()

class QuestionRequest(BaseModel):
  question: str

SYSTEM_PROMPT = """
You are a SQL assistant. Return ONLY a single PostgreSQL SELECT query.

Rules:
- NO markdown formatting (no ```sql or ```)
- NO explanations
- NO comments
- NO semicolons
- Start with SELECT
- Use these exact column names with double quotes: "ORDERNUMBER", "QUANTITYORDERED", "PRICEEACH", "ORDERLINENUMBER", "SALES", "ORDERDATE", "DAYS_SINCE_LASTORDER", "STATUS", "PRODUCTLINE", "MSRP", "PRODUCTCODE", "CUSTOMERNAME", "PHONE", "ADDRESSLINE1", "CITY", "POSTALCODE", "COUNTRY", "CONTACTLASTNAME", "CONTACTFIRSTNAME", "DEALSIZE"

Example output format:
SELECT "SALES" FROM sales WHERE "COUNTRY" = 'USA' LIMIT 10
"""




SYSTEM_PROMPT_SUMMARY = """
You are a helpful data analyst. Given a user's question and a SQL result (in JSON format), provide a clear, concise explanation of what the data means.
"""

def clean_sql_query(raw_query):

  cleaned = raw_query.strip()
  cleaned = cleaned.replace('```sql', '').replace('```','')
  cleaned = cleaned.replace('`','')

  if cleaned.endswith(';'):
    cleaned = cleaned[:-1]
  
  cleaned = cleaned.strip()

  return cleaned


@app.post("/ask")
async def ask_question(data:QuestionRequest):

  try:

    response = client.chat.completions.create(
      model = "gpt-3.5-turbo",
      messages=[
        {"role":"system" , "content": SYSTEM_PROMPT},
        {"role":"user", "content" : data.question}

      ]
    )
    sql_query = response.choices[0].message.content.strip()
    sql_query = clean_sql_query(sql_query)

    if not sql_query.upper().startswith('SELECT'):
            raise HTTPException(status_code=400, detail="Invalid SQL query generated - must start with SELECT")
    #here we are querying the database of the company

    try:
      with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        rows = [dict(row._mapping) for row in result]
    except Exception as db_error:
            raise HTTPException(status_code=400, detail=f"Database query failed: {str(db_error)}")

    
    explanation_response =client.chat.completions.create(
      model = "gpt-3.5-turbo",
      messages=[
        {"role" :"system","content": SYSTEM_PROMPT_SUMMARY},
        {"role":"user","content": f"User asked: {data.question}\n Here are the results:{rows}"}
      ]
    )

    summary =explanation_response.choices[0].message.content.strip()


    return {
      "question" : data.question,
      "sql" :sql_query,
      "result" : rows,
      "summary" :summary
    }
  
  except Exception as e:
    raise HTTPException(status_code=500,detail=str(e))
  
