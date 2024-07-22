Custom Chatbot

Steps to test : 
- create virtual environment
- install all libs from requirements.txt
- set .env file with required API keys and access tokens
- run chroma using "chroma run"
- run main.py using "streamlit run main.py"

It is a custom chatbot. Based on the data you feed, it can answer correctly(percentage of correctness will be based on the model you used) using ingested data.

How it works

- Put many urls to ask about what you want(for more than one url, using "," after one url)
- Click Enter from keyboard or Click "Ingest Data" button. Wait until data is ingested
- if you see "Data Ingested", you can start asking whatever you want
- Have fun to test it