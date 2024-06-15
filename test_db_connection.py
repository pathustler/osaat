import os
import pyodbc

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('AZURE_SQL_SERVER')};"
    f"DATABASE={os.getenv('AZURE_SQL_DATABASE')};"
    f"UID={os.getenv('AZURE_SQL_USER')};"
    f"PWD={os.getenv('AZURE_SQL_PASSWORD')};"
    f"TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Connection successful")
except Exception as e:
    print(f"Error: {e}")