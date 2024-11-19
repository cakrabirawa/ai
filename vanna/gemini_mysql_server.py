#Python program to convert natural language to SQL query and execute it.
# Requirements
# python 3.x
# Packages required are
#pip install -U google -generativeai
#pip install pyodbc

import google.generativeai as genai
import mysql.connector


# API key for Gemini Generative AI, you can get it from the below link. 
# https://aistudio.google.com/app/apikey

api_key = "AIzaSyAqDgK8o1x1Qmm9jli5Lh1b7OZf0jgtR9M"
genai.configure(api_key=api_key)
#api key initialization

model = genai.GenerativeModel("gemini-pro")
#selecting the instance of gemini model and initializing the connection to Gemini

# Connect to MS SQL Server 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="P@ssw0rd@!",
  database="openposcinunukdb2"
)
#creates a cursor object that allows you to execute SQL queries 
cursor = mydb.cursor()

print ("Connection Opened !")

# Function to execute SQL query and fetch results
def execute_query(sql_query):
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return result

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
prompt = [
    """
    You are an expert in converting English questions to MS SQL query!
    The SQL database has the name tm_kota and has the following columns - nIdKota, sNamaKota
       \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM tm_kota;
    \nExample 2 - Tell me all the city started with J letter?, 
    the SQL command will be something like this SELECT * FROM tm_kota where sNamaKota like '%J'; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Natural language query to be converted to SQL as input to Gemini
user_query = "Show count of data"

# Generate SQL query from the natural language query using the Generative AI model
response = model.generate_content([prompt[0], user_query])

print (response.text)

# Execute the generated SQL query
results = execute_query(response.text)

print(results)
#unformatted results from the database

# Format and print the query results
formatted_results = format_results(results)

print("Query Results:")
for row in formatted_results:
    print("------------------------------------")
    for key, value in row.items():
        print(f"{key}: {value}")
    print("------------------------------------")

# Close the database connection
mydb.close()