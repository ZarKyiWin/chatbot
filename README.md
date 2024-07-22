# Custom Chatbot 

## Steps to test

### Create Virtual Environment 
```batch
python -m venv virtualenv
```
### Install all libs from requirements.txt
```batch
\venv\Scripts\activate
```
### Run chromadb
```batch
chroma run --path ./db_path
```
### Run main.py 
```batch
streamlit run main.py
```

### It is a custom chatbot. Based on the data you feed, it can answer correctly(percentage of correctness will be based on the model you used) using ingested data.

## How it works

- Put many urls to ask about what you want(for more than one url, using "," after one url)
- Click "Ingest Data" button. Wait until data is ingested
- If you see "Data Ingested", you can start asking whatever you want
- Have fun to test it
