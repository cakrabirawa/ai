# Python program to connect to google gemini model
# Requirements
# python 3.x
# pip install google-generativeai
import google.generativeai as genai
import os

# Replace with your own API key
# Get the google API key: https://aistudio.google.com/app/apikey
# Create a new system environmental variable with name GOOGLE-API-KEY-VID and in the value paste the google API key
google_api_key = "AIzaSyAqDgK8o1x1Qmm9jli5Lh1b7OZf0jgtR9M"
genai.configure(api_key=google_api_key)
# Initialize connection to Gemini
model=genai.GenerativeModel("gemini-pro")

response = model.generate_content("sebutkan 3 kota besar di indonesia, beserta jumlah penduduknya dan suku paling besar yang mendiaminya")

print(response.text)