import os
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go

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
    'centerback': 'centerbacks.csv',
    'fullback': 'fullbacks.csv',
    'midfielder': 'midfielders.csv',
    'winger': 'wingers.csv',
    'striker': 'strikers.csv'
}
ages_min = list(range(15, 41))
ages_max = list(range(15, 41))


#df_select = get_select_data()
option0_club_name1 = st.text_input('Your club name :', 'Club Brugge') # Mettre un espace vide ??????????
option0_club_name2 = st.text_input('Club playing style :', 'Man City') # A supprimer plus tard

option1_game_style = st.selectbox('Select a game style', game_styles)
#option2_position = st.selectbox('Select a position', positions)
option2_selected_position = st.selectbox('Select a position', options=list(position_to_file.keys()))
# Load the corresponding DataFrame
file_name = position_to_file[option2_selected_position]
dataframe_path = f'raw_data/{file_name}'
selected_df = pd.read_csv(dataframe_path)

option3_ages_min = st.selectbox('Select the player minimum age ', ages_min)
option4_ages_max = st.selectbox('Select the player maximum age ', ages_max)

option5_market_value = st.number_input('Select market value')
option6_expected_market_value = st.number_input('Select expected market value')



#filtered_df = df_select[(df_select['Game style'] == option1) & (df_select['Position'] == option2) & (df_select['Age_min'] == option3)                        & (df_select['Age_max'] == option4)]
filtered_df = pd.DataFrame({
        'Game style': option1_game_style,
        'Position': option2_selected_position,
        'Age min': option3_ages_min,
        'Age max': option4_ages_max,
        'Market value': option5_market_value,
        'Expected market value': option6_expected_market_value
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

scaled_df_kmeans = pd.read_csv('raw_data/scaled_df_kmeans.to_csv')
