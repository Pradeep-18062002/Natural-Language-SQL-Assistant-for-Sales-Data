# SalesBot: Natural Language Query System for Sales Data

SalesBot is an AI-powered backend that allows users to ask natural language questions about structured sales data. The system translates user queries into SQL, executes them on a PostgreSQL database, and summarizes the results using OpenAI's GPT models.

---

## Features

- FastAPI backend with OpenAI GPT integration
- Converts user questions into SQL using GPT-3.5
- Executes SQL queries on a PostgreSQL database (Neon)
- Uses GPT to explain the returned query results
- Interactive API testing available at `/docs`

---

## Tech Stack

- Python 3.10+
- FastAPI
- OpenAI GPT-3.5 API
- PostgreSQL (via Neon)
- SQLAlchemy
- Pydantic
- Uvicorn

---

project/
├── load_db.py         # Script to load CSV data into PostgreSQL
├── api.py             # FastAPI backend for question answering
├── .env               # Environment variables (OpenAI key, DB URL)
├── requirements.txt   # Python dependencies
└── Sales Data.csv     # Sample sales dataset


Sample Dataset Schema
Table: sales

Column	Type	Description
ORDERNUMBER	int	Order ID
QUANTITYORDERED	int	Number of items ordered
PRICEEACH	float	Price per item
SALES	float	Total sale value
ORDERDATE	string	Date of order in DD/MM/YYYY format
PRODUCTLINE	string	Product category
CUSTOMERNAME	string	Customer name
DEALSIZE	string	Size of the deal (Small/Medium/Large)

To-Do
Add authentication for the API

Create a frontend interface

Improve SQL validation and safety

Add support for multi-table queries

Add Docker support for deployment

License
This project is licensed under the MIT License.

