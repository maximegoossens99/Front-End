import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

scaler = joblib.load('models/minmax_scaler.joblib')
km = joblib.load('models/knn_model.joblib')
nbrs = joblib.load('models/nearest_neighbors_model.joblib')
scaled_df_kmeans = pd.read_csv('raw_data/scaled_df_kmeans.csv')


st.title('Football Fictive Player Processing')

# Input Request
st.markdown("""
# Inputs:
## Player Characteristics
""")

# Define your game styles, positions, and age ranges
game_styles = ['Counter-Attacking Prowess', 'High-Pressing Havoc', 'Defensive Fortress',
               'Wing Dominance', 'Possession with Purpose', 'Youthful Energy and High Intensity',
               'Midfield Maestros']

# Mapping of positions to their corresponding CSV files
centerback_df = pd.read_csv('raw_data/centerback.csv')
fullback_df = pd.read_csv('raw_data/fullback.csv')
midfielder_df = pd.read_csv('raw_data/midfielder.csv')
winger_df = pd.read_csv('raw_data/winger.csv')
striker_df = pd.read_csv('raw_data/striker.csv')
perfect_df = pd.read_csv('raw_data/final_df.csv')


position_to_file = {
    'centerback': centerback_df,
    'fullback': fullback_df,
    'midfielder': midfielder_df,
    'winger': winger_df,
    'striker': striker_df
}

ages_min = list(range(15, 41))
ages_max = list(range(15, 41))

# Streamlit input widgets
option0_club_name1 = st.text_input('Your club name:', 'Club Brugge')
option0_club_name2 = st.text_input('Club playing style :', 'Man City') # A supprimer plus tard

option1_game_style = st.selectbox('Select a game style', game_styles)
option2_selected_position = st.selectbox('Select a position', options=list(position_to_file.keys()))


option3_ages_min = st.selectbox('Select the player minimum age', ages_min)
option4_ages_max = st.selectbox('Select the player maximum age', ages_max)
option5_market_value = st.number_input('Select market value')
option6_expected_market_value = st.number_input('Select expected market value')

# Display the selected parameters
filtered_df = pd.DataFrame({
    'Game style': [option1_game_style],
    'Position': [option2_selected_position],
    'Age min': [option3_ages_min],
    'Age max': [option4_ages_max],
    'Market value': [option5_market_value],
    'Expected market value': [option6_expected_market_value]
})

st.write('Player parameters:')
st.write(filtered_df)


# NOTES ET MODIFICATIONS A APPORTER AU CODE !
#Changer les paramètres : team_1 -> option0_club_name1 ...
#Changer les paramètres : team_2 -> option1_game_style
#Changer les paramètres : position -> option2_selected_position
#num_neighbors doit être egal a 1000 pour pouvoir filter apres !
# voir le probleme avec le scaler !(minmaxscaler)
#choisir le bon dataframe (voir si noms dedans (devrait deja etre le cas))



# Define your find_closest_players function here
# Include all necessary imports and function definitions inside the function
def find_closest_players(position, team_1, team_2, num_neighbors):
    # Your function implementation...
    # For now, I'll return a placeholder DataFrame for demonstration
    # Replace this with the actual logic of your function
    def custom_scaler(dfgf_no_name):
        total_score = dfgf_no_name.sum(axis=1)
        scaled_dfgf_no_name = dfgf_no_name.div(total_score, axis=0)
        total_score = scaler.transform(total_score.values.reshape(-1, 1)).flatten()
        return total_score, scaled_dfgf_no_name
    def compare_teams(df, team1, team2):
        df1 = df[df['club'] == team1]
        df2 = df[df['club'] == team2]
        df1.drop(columns=['club'], inplace=True)
        df2.drop(columns=['club'], inplace=True)
        subtracted_df = df2.sub(df1, fill_value=0)
        row_sums = subtracted_df.sum(axis=0)
        total_score, result = custom_scaler(pd.DataFrame(row_sums).T.drop(columns=['club_rating']))
        result = result.clip(lower=0)
        result['scaled_total_score'] = abs(total_score)
        name = pd.DataFrame(data=["Nino_M"], columns=['name'])
        result = name.join(result)
        st.write(result) # to remove
        #return result
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
    new_column_names = ['centerback', 'fullback', 'goalkeepers', 'midfielder', 'striker', 'winger']
    positions.columns = new_column_names
    # Set the diagonal elements to 1
    np.fill_diagonal(positions.values, 1)
    final_df = positions.join(foots, how='cross')
    Nino = compare_teams(position, team_1, team_2)
    Nino = Nino.join(final_df, how='cross')
    series = pd.Series([f'Nino_M_{i}' for i in range(24)])
    Nino.name = series
    Nino = Nino[Nino.goalkeepers != 1]
    st.write(Nino)
    Nino.drop(columns=['goalkeepers', 'goalkeeping_abilities'], inplace=True)
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
        # player_stats = player_stats.drop(columns='label')
        # Fit the NearestNeighbors model
        # Find the nearest neighbors
        distances, indices = nbrs.kneighbors(player_stats)
        # Get the names of similar players
        # Exclude the first one if it's the player themselves
        similar_players_indices = indices.flatten()
        similar_players = scaled_df_kmeans.iloc[similar_players_indices].sort_values(by='scaled_total_score',ascending=False)[['name', 'scaled_total_score']]
        #by='scaled_total_score' bPREVIOUS SORTING
        results.append(similar_players)
    final_result = pd.concat(results).sort_values(by='scaled_total_score', ascending=False)
    st.write(perfect_df)
    final_result = pd.merge(perfect_df, final_result, how='inner', left_on='name_y', right_on='name')
    st.write(final_result)
    return final_result


# Trigger analysis based on user input
if st.checkbox('Start player analysis'):
    # Loading animation code
    with st.spinner('Performing analysis...'):
        # Call your find_closest_players function
        closest_players_result = find_closest_players(position_to_file[option2_selected_position], option0_club_name1, option0_club_name2, 5)

        # Display the results using Plotly graphs
        for index, row in closest_players_result.iterrows():
            fig = go.Figure()

            # Example Plotly graph - replace with your actual graph code
            fig.add_trace(go.Bar(x=['Player', 'Score'], y=[row['Player'], row['Score']]))

            st.plotly_chart(fig)

            # Limit to 5 graphs
            if index >= 4:
                break

    st.success('Player analysis done!')


if st.checkbox('Show Details of Selected Players'):
    if 'closest_players_result' in locals():
        st.write(closest_players_result)
    else:
        st.warning("Please run the analysis first to see details.")

# Allow users to download the results as CSV
if st.checkbox('Download Results as CSV'):
    if 'closest_players_result' in locals():
        csv = closest_players_result.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='closest_players.csv',
            mime='text/csv',
        )
    else:
        st.warning("Please run the analysis first to download the data.")

# About section
st.markdown("""
## About this Tool
This tool is designed for football analysts and enthusiasts to find players with similar characteristics and performance metrics. By inputting a player's details and selecting specific criteria, the tool uses advanced data analysis techniques to identify comparable players and visualize their similarities.
""")

# Add any additional code or features here...

# End of Streamlit app
