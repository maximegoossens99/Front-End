import streamlit as st
import pandas as pd

import streamlit as st

# ... (your existing imports and setup code)

# Define your game styles, positions, and age ranges
# ... (your existing definitions)

# Streamlit input widgets laid out in three columns
st.title('Football fictive player processing')

# Input Request
st.markdown("""
# Inputs:
## Player caracteristics """
            )
#@st.experimental_memo
#def get_select_data():
game_styles = ['Counter-Attacking Prowess', 'High-Pressing Havoc', 'Defensive Fortress',
                   'Wing Dominance', 'Possession with Purpose', 'Youthful Energy and High Intensity',
                   'Midfield Maestros']
#positions = ['centerback', 'fullback', 'midfielder', 'winger', 'striker']
# Mapping of positions to their corresponding CSV files
position_to_file = {
    'centerback': 'centerback.csv',
    'fullback': 'fullback.csv',
    'midfielder': 'midfielder.csv',
    'winger': 'winger.csv',
    'striker': 'striker.csv'
}
ages_min = list(range(15, 41))
ages_max = list(range(15, 41))

col1, col2, col3 = st.columns(3)

with col1:
    option0_club_name1 = st.text_input('Your club name:', 'Club Brugge')
    option1_game_style = st.selectbox('Select a game style', game_styles)
    option3_ages_min = st.selectbox('Select the player minimum age', ages_min)

with col2:
    option0_club_name2 = st.text_input('Club playing style:', 'Man City')  # To be removed later
    option2_selected_position = st.selectbox('Select a position', options=list(position_to_file.keys()))
    option4_ages_max = st.selectbox('Select the player maximum age', ages_max)

with col3:
    option5_market_value = st.number_input('Select market value')
    option6_expected_market_value = st.number_input('Select expected market value')

# ... (the rest of your code)
