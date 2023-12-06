import os
import streamlit as st
import pandas as pd
import numpy as np
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
    'centerback': 'centerback.csv',
    'fullback': 'fullback.csv',
    'midfielder': 'midfielder.csv',
    'winger': 'winger.csv',
    'striker': 'striker.csv'
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

scaled_df_kmeans = pd.read_csv('raw_data/scaled_df_kmeans.csv')



#-------------------------------------------------------------------------------
def find_closest_players(position, team_1, team_2, num_neighbors):
    def custom_scaler(dfgf_no_name):
        total_score = dfgf_no_name.sum(axis=1)
        scaled_dfgf_no_name = dfgf_no_name.div(total_score, axis=0)
        total_score = scaler.transform(total_score.values.reshape(-1, 1)).flatten()
        return total_score, scaled_dfgf_no_name
    def compare_teams(df, team1, team2):
        df1 = df.loc[team1]
        df2 = df.loc[team2]
        total_score, result = custom_scaler(pd.DataFrame(df1.subtract(df2)).T.drop(columns=['club_rating']))
        result = result.clip(lower=0)
        result['scaled_total_score'] = abs(total_score)
        name = pd.DataFrame(data=["Nino_M"], columns=['name'])
        result = name.join(result)
        return result
    # Specify the dimensions of the DataFrame
    rows = 4
    columns = 4
    # Create a DataFrame filled with zeros
    foots = pd.DataFrame(np.zeros((rows, columns)), columns=[f'col{i+1}' for i in range(columns)])
    new_column_names = ['either_left', 'either_right', 'left', 'right']
    foots.columns = new_column_names
    # Set the diagonal elements to 1
    np.fill_diagonal(foots.values, 1)
    # Specify the dimensions of the DataFrame
    rows = 6
    columns = 6
    # Create a DataFrame filled with zeros
    positions = pd.DataFrame(np.zeros((rows, columns)), columns=[f'col{i+1}' for i in range(columns)])
    new_column_names = ['centerback', 'fullback', 'midfielder', 'striker', 'winger']
    positions.columns = new_column_names
    # Set the diagonal elements to 1
    np.fill_diagonal(positions.values, 1)
    final_df = positions.join(foots, how='cross')
    Nino = compare_teams(position, team_1, team_2)
    Nino = Nino.join(final_df, how='cross')
    series = pd.Series([f'Nino_M_{i}' for i in range(24)])
    Nino.name = series
    Nino = Nino[Nino.goalkeeper != 1]
    Nino.drop(columns=['goalkeeper', 'goalkeeping_abilities'], inplace=True)
    Nino.reset_index(inplace=True, drop=True)
    data = Nino
    #if player_name not in data['name'].values:
    #r    return f"Player '{player_name}' not found in the dataset."
    feature_columns = data.columns.drop('name')
    results = []
    for player_name in Nino.name:
        # Extract the specified player's statistics
        player_stats = data[data['name'] == player_name].drop(columns='name')
        player_stats['label'] = km.predict(player_stats)
        # Drop the 'label' column before fitting the model
        player_stats = player_stats.drop(columns='label')
        # Fit the NearestNeighbors model
        nbrs = NearestNeighbors(n_neighbors=num_neighbors + 1).fit(scaled_df_kmeans[feature_columns])
        # Find the nearest neighbors
        distances, indices = nbrs.kneighbors(player_stats)
        # Get the names of similar players
        # Exclude the first one if it's the player themselves
        similar_players_indices = indices.flatten()
        similar_players = scaled_df_kmeans.iloc[similar_players_indices].sort_values(by='scaled_total_score',ascending=False)[['name', 'scaled_total_score']]
        #by='scaled_total_score' bPREVIOUS SORTING
        results.append(similar_players)
    final_result = pd.concat(results).sort_values(by='scaled_total_score', ascending=False)
    return final_result
