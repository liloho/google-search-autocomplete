import streamlit as st

from data_processing import *
import matplotlib.pyplot as plt


#==== Main App
st.title('Google Search Autocomplete')
st.markdown("### Fun")

#Inputs
prompt = "Why do cyclists"
country = "uk" 
seed = [c for c in ascii_lowercase]


data = get_suggestions(prompt, seed, country)
data_for_plot = get_relevant_results(data, prompt, seed)
table = get_table_view(data, seed, prompt)

st.write(table)
st.write(data_for_plot)

