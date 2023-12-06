import os
import streamlit as st
import pandas as pd

# Title and Introduction
st.markdown("""
# Moneyball project applied to football
## For companies and private customers
- Dataframe size : + 170 000 players
- Number of features : +15 features
- *You can contact our secretary for any questions: **Maxime Goossens** [LinkedIn](https://be.linkedin.com/in/maximegoossens)*
""")

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Clients in 2023", "75", "+33")
col2.metric("Followers (insta)", "57K", "+47K")
col3.metric("Salaire Maxime", "$15", "+4.87%")



# SLIDER DEMO
#@st.cache
#def get_slider_data():
#    return pd.DataFrame({'Age of the player': list(range(15, 40))})
#
#df_slider = get_slider_data()
#option = st.slider('Select the player age', 15, 40)










# TODO: Call the API using the user's input
#   - url is already defined above
#   - create a params dict based on the user's input
#   - finally call your API using the requests package


# TODO: retrieve the results
#   - add a little check if you got an ok response (status code 200) or something else
#   - retrieve the prediction from the JSON


# TODO: display the prediction in some fancy way to the user


# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page
