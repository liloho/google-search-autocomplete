import requests
from bs4 import BeautifulSoup
from string import ascii_lowercase
import time
import pandas as pd
import streamlit as st

#get first 3 suggestions from Google search autocomplete
@st.cache_data
def get_suggestions(prompt, seed, country):
    keywords = [prompt + " " + c for c in seed]
    data = []
    for kw in keywords:
        r = requests.get('http://suggestqueries.google.com/complete/search?output=toolbar&hl={}&q={}'.format(country,kw))
        soup = BeautifulSoup(r.content, 'html.parser')
        results = [result['data'] for result in soup.find_all('suggestion')]
        data.append(results[0:3])
        time.sleep(0.02)
    return data

#derive first relevant match for viz
def get_relevant_results(data, prompt, seed):
    df = {"letter": [c.upper() for c in seed], "result":[]}
    for kw, result in enumerate(data):
        success = 0
        for i in range(len(result)):
            if success==0:
                if prompt.lower() in result[i]:
                    df["result"].append(result[i])
                    success+=1
        if success==0:
            df["result"].append("*")
            
    df = pd.DataFrame.from_dict(df)
    return df

#clean data for table view
def get_table_view(data, seed, prompt):
    table = pd.DataFrame.from_dict(data)
    table = table.rename(columns={0:"Suggestion 1", 1:"Suggestion 2", 2:"Suggestion 3"})
    table["Prompt"] = [prompt + " " + c.upper() for c in seed]
    table = table[["Prompt"]+list(table.columns[:3])]
    return table