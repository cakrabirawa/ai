#Python program to convert natural language to SQL query and execute it.
# Requirements
# python 3.x
# Packages required are
#pip install -U google -generativeai
#pip install pyodbc

import pyodbc
import google.generativeai as genai


# API key for Gemini Generative AI, you can get it from the below link. 
# https://aistudio.google.com/app/apikey

api_key = "AIzaSyAqDgK8o1x1Qmm9jli5Lh1b7OZf0jgtR9M"
genai.configure(api_key=api_key)
#api key initialization

model = genai.GenerativeModel("gemini-pro")
#selecting the instance of gemini model and initializing the connection to Gemini

# Connect to MS SQL Server 
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=ADO\\TEW_SQLEXPRESS;'
                      'DATABASE=cungukdb;'
                      'UID=sa;'
                      'PWD=P@ssw0rd@!;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
#creates a cursor object that allows you to execute SQL queries 


# Function to execute SQL query and fetch results
def execute_query(sql_query):
    cursor.execute(sql_query)
    return cursor.fetchall()

# Function to format SQL query results
def format_results(results):
    columns = [column[0] for column in cursor.description]
    #extracts the column names from the cursor's description attribute and stores them in the columns list.

    formatted_results = []
    #an empty list

    for row in results:
        formatted_row = {}
        for i, value in enumerate(row):
            formatted_row[columns[i]] = value
        formatted_results.append(formatted_row)

    return formatted_results

# Sample prompt for the Generative AI model
prompt = """
    terjemahkan pertanyaan ke dalam bahasa indonesia, lakukan konversi pertanyaan ke dalam struktur sql, output juga menyertakan lama pencarian, saya memiliki tabel test01, test02, tempe01 dan 365_loging
    """
# Natural language query to be converted to SQL as input to Gemini
user_query = "tampilkan 5 penjualan terakhir lengkap dengan id produk dan nama produk"

# Generate SQL query from the natural language query using the Generative AI model
response = model.generate_content([prompt[0], user_query])

print (response.text)

# Execute the generated SQL query
#results = execute_query(response.text.replace("```", "").replace("sql", ""))

#print(results)
#unformatted results from the database

# Format and print the query results
#formatted_results = format_results(results)

#print("Query Results:")
#for row in formatted_results:
#    print("------------------------------------")
#    for key, value in row.items():
#        print(f"{key}: {value}")
#    print("------------------------------------")

# Close the database connection
conn.close()