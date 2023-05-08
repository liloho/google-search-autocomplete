from msilib.sequence import tables
import streamlit as st
from iso3166 import countries
from data_processing import *
from plotting import *

st.set_page_config(
    page_title="Ask what",
    page_icon="❔",
    layout="wide",
    initial_sidebar_state="collapsed"
     )

country_names = []
for c in countries:
       country_names.append(c[0])

#=== Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("Put in any prompt you like and visualise Google autocomplete suggestions for each letter.")
    st.subheader("Get in touch")
    st.markdown("Made by Lisa Hornung, I'm on [Github](https://github.com/Lisa-Ho), [Mastodon](https://fosstodon.org/@LisaHornung), [Linkedin](https://www.linkedin.com/in/lisa-maria-hornung/), and [Twitter](https://twitter.com/LisaHornung_)")

#==== Main App
col1a, col1b,col1c = st.columns([0.225,0.55,0.225])
with col1b:
    st.title('Ask What?')
    st.markdown("#### Visualise Google search autocomplete suggestions")
    st.markdown("Note: Currently limited to Latin alphabets")

    with st.form(key='update prompt'):
        col1b_1, col1b_2 = st.columns([3,2])
        with col1b_1:
            prompt = st.text_input("Prompt", "What is the best")
        with col1b_2:
            country = st.selectbox('Country', options=country_names, index=235)
            country_code = countries.get(country)[1]
        seed = [c for c in ascii_lowercase]
        st.form_submit_button('Update')

    #get and transform data based on inputs
    data = get_suggestions(prompt, seed, country_code)
    data_for_plot = get_relevant_results(data,  seed, prompt)
    table = get_table_view(data, seed, prompt)

#create and visualise plot
fig = plot_circular_outward(data_for_plot, prompt)
col2a, col2b,col2c = st.columns([0.225,0.55,0.225])
with col2b:
    st.write(fig)

    plt.savefig("google-search-autocomplete.png", bbox_inches="tight", dpi=300, pad_inches=1)
    with open("google-search-autocomplete.png", "rb") as image:
        png = st.download_button(
            label="Download png",
            data=image,
            file_name="google-search-autocomplete.png",
            mime="image/png"
        )
    st.write("")
    with st.expander("Explore top three suggestions"):
        st.dataframe(table, use_container_width=False)

