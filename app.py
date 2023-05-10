import streamlit as st
from iso3166 import countries
from data_processing import *
from plotting import *

st.set_page_config(
    page_title="Search Roulette",
    page_icon="❔",
    layout="wide",
    initial_sidebar_state="collapsed"
     )

country_names = []
for c in countries:
       country_names.append(c[0])

#==== Main App
col1a, col1b,col1c = st.columns([0.225,0.55,0.225])
with col1b:
    st.title('Search Roulette')
    st.markdown("#### Google search autocomplete suggestions for any prompt")
    st.markdown("Note: Currently limited to Latin alphabets")

    with st.form(key='update prompt'):
        col1b_1a, col1b_1b = st.columns([3,2])
        with col1b_1a:
            prompt = st.text_input("Prompt", "What is the best")
        with col1b_1b:
            country = st.selectbox('Country', options=country_names, index=235)
            country_code = countries.get(country)[1]
        seed = [c for c in ascii_lowercase]
        
        col1b_2a, col1b_2b, col1b_2c, col1b_2d  = st.columns([1,1,1,2])
        with col1b_2a:
                bg_colour = st.color_picker("Background colour", "#F9F9F9")
        with col1b_2b:
                font_colour = st.color_picker("Font colour", "#000000")
        with col1b_2c:
                line_colour = st.color_picker("Line colour", "#000000")
        st.form_submit_button('Update')

    #get and transform data based on inputs
    data = get_suggestions(prompt, seed, country_code)
    data_for_plot = get_relevant_results(data,  seed, prompt)
    table = get_table_view(data, seed, prompt)

#create and visualise plot
fig = plot_circular_outward(data_for_plot, prompt, bg_colour, font_colour, line_colour)
col2a, col2b,col2c = st.columns([0.225,0.55,0.225])
with col2b:
    st.write(fig)

    plt.savefig("google-search-autocomplete.png", bbox_inches="tight", dpi=300, pad_inches=1)
    with open("google-search-autocomplete.png", "rb") as image:
        png = st.download_button(
            label="Download image",
            data=image,
            file_name="google-search-autocomplete.png",
            mime="image/png"
        )
    st.write("")
    with st.expander("Explore first three suggestions"):
        st.dataframe(table, use_container_width=False)

    st.write("")
    st.divider()
    st.markdown("Made by Lisa Hornung, follow me on [Github](https://github.com/Lisa-Ho), [Mastodon](https://fosstodon.org/@LisaHornung), [Linkedin](https://www.linkedin.com/in/lisa-maria-hornung/), and [Twitter](https://twitter.com/LisaHornung_)")