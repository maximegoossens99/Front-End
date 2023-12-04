import os
import streamlit as st
import pandas as pd

# Title and Introduction
st.markdown("""
# Moneyball project applied to football
## For companies and private customers
- Companies : 1000€ / mission
- Private customers : 1500€ / mission
- *You can contact our secretary for any questions: **Maxime Goossens** [LinkedIn](https://be.linkedin.com/in/maximegoossens)*
""")

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Clients in 2023", "75", "+33")
col2.metric("Followers (insta)", "57K", "+47K")
col3.metric("Salaire Maxime", "$15", "+4.87%")

# Input Request
st.markdown("""
# Inputs:
## Player caracteristics """
            )

# SLIDER DEMO
#@st.cache
#def get_slider_data():
#    return pd.DataFrame({'Age of the player': list(range(15, 40))})
#
#df_slider = get_slider_data()
#option = st.slider('Select the player age', 15, 40)

#@st.experimental_memo
#def get_select_data():
game_styles = ['Counter-Attacking Prowess', 'High-Pressing Havoc', 'Defensive Fortress',
                   'Wing Dominance', 'Possession with Purpose', 'Youthful Energy and High Intensity',
                   'Midfield Maestros']
positions = ['goalkeeper', 'centerback', 'fullback', 'midfielder', 'winger', 'striker']
ages_min = list(range(15, 41))
ages_max = list(range(15, 41))

#return pd.DataFrame({
#        'Game style': game_styles * len(positions) * len(ages_min),
#        'Position': positions * len(game_styles) * len(ages_min),
#        'Age_min': ages_min * len(game_styles) * len(positions),
#        'Age_max': ages_max * len(game_styles) * len(positions)
#
#    })'''


#df_select = get_select_data()
option1 = st.selectbox('Select a game style', game_styles)
option2 = st.selectbox('Select a position', positions)
option3 = st.selectbox('Select the player minimum age ', ages_min)
option4 = st.selectbox('Select the player maximum age ', ages_max)

option5 = st.number_input('Select market value')
option6 = st.number_input('Select expected market value')

#filtered_df = df_select[(df_select['Game style'] == option1) & (df_select['Position'] == option2) & (df_select['Age_min'] == option3)                        & (df_select['Age_max'] == option4)]
filtered_df = pd.DataFrame({
        'Game style': option1,
        'Position': option2,
        'Age min': option3,
        'Age max': option4,
        'Market value': option5,
        'Expected market value': option6
}, index=[0])
'Player parameters :'
st.write(filtered_df)

if st.checkbox('Start player analysis'):
    import time

    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    'Player analysis done !'









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
