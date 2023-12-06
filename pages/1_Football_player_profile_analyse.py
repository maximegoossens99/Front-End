import os
import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go

#Club logo IMAGE
#st.write('This is page 1')
#logo_affichage = ("![Foo](https://tmssl.akamaized.net/images/wappen/small/281.png?lm=1467356331)")
#st.markdown(logo_affichage) # coder l'affichage du logo en fonction du club !

# Load the dataset from the raw_data folder
scaled_df_kmeans = pd.read_csv('raw_data/scaled_df_kmeans.to_csv')
#chager peut être la taille des caractères pour avoir tout en lover ce qui faciite les recherches

# Streamlit interface
st.title('Football player profile analyse')

# User inputs
player_name = st.text_input('Enter a player name:')
num_neighbors = st.number_input('Number of neighbors:', min_value=1, max_value=20, value=5)

# Define your find_closest_players function here
def find_closest_players(player_name, num_neighbors, data, feature_columns):
    if player_name not in data['name'].values:
        return f"Player '{player_name}' not found in the dataset."

    # Extract the specified player's statistics
    player_stats = data[data['name'] == player_name][feature_columns].to_numpy()

    # Fit the NearestNeighbors model
    nbrs = NearestNeighbors(n_neighbors=num_neighbors + 1).fit(data[feature_columns])

    # Find the nearest neighbors
    distances, indices = nbrs.kneighbors(player_stats)

    # Get the names of similar players
    similar_players_indices = indices.flatten()
    if similar_players_indices[0] == data[data['name'] == player_name].index[0]:
        similar_players_indices = similar_players_indices[1:]
    else:
        similar_players_indices = similar_players_indices[:-1]

    # Extract similar players data
    return data.iloc[similar_players_indices]

# Use all columns except 'name' for finding neighbors
all_feature_columns = scaled_df_kmeans.columns.drop('name')

# Define the subset of features for the radar chart
radar_features = ['shooting', 'dribbling_control', 'passing_vision',
                  'tackling_interception', 'aerial_defense', 'speed_agility',
                  'strength_stamina', 'decision_making', 'work_ethic_effort',
                  'leadership', 'teamwork']


# Find and display closest players
if st.button('Find Closest Players'):
    closest_players = find_closest_players(player_name, num_neighbors, scaled_df_kmeans, all_feature_columns)
    st.dataframe(closest_players)

    # Player's own stats for radar features
    player_stats = scaled_df_kmeans[scaled_df_kmeans['name'] == player_name][radar_features].iloc[0]

    # Create and display radar charts, skipping the first player
    for i, (index, row) in enumerate(closest_players.iterrows()):
        if i == 0:  # Skip the first player's chart
            continue

        fig = go.Figure()

        # Add trace for the input player
        fig.add_trace(go.Scatterpolar(
            r=player_stats.values,
            theta=radar_features,
            fill='toself',
            name=player_name
        ))

        # Add trace for the closest player
        fig.add_trace(go.Scatterpolar(
            r=row[radar_features].values,
            theta=radar_features,
            fill='toself',
            name=row['name']
        ))

        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True
                )),
            showlegend=True,
            title=f"Comparison: {player_name} vs {row['name']}"
        )

        # Show the plot
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")

# ADD COOLUMS FOR THE DISPLAY OF THE INFORMATION (GRAPHICS) !!!!
