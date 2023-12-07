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

col1, col2 , col3= st.columns(3)

with col1:
    option0_club_name1 = st.text_input('Club name:', 'Club Brugge')
    option3_ages_min = st.selectbox('Minimum age', ages_min)
    
    option5_market_value = st.number_input('Market value')


with col2:
    #option0_club_name2 = st.text_input('Club playing style:', 'Man City')  # To be removed later
    option1_game_style = st.selectbox('Game style', game_styles)
    option4_ages_max = st.selectbox('Maximum age', ages_max)

    option6_expected_market_value = st.number_input('Expected market value')

with col3:
    option2_selected_position = st.selectbox('Position', options=list(position_to_file.keys()))



# ... (the rest of your code)
