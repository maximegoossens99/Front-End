import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from streamlit.components.v1 import html

#st.markdown("""
#<style>
#    [data-testid=stSidebar] {
#        background-color: #ff000050;
#    }
#</style>
#""", unsafe_allow_html=True)

# Initialize session state
if 'input_values' not in st.session_state:
    st.session_state.input_values = {}

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

scaler = joblib.load('models/minmax_scaler.joblib')
km = joblib.load('models/knn_model.joblib')
nbrs = joblib.load('models/nearest_neighbors_model.joblib')
scaled_df_kmeans = pd.read_csv('raw_data/scaled_df.csv')


st.title('Football Fictive Player Processing')

# Input Request
st.markdown("""
# Inputs:
## Player Characteristics
""")

# Define your game styles, positions, and age ranges
#game_styles = ['Counter-Attacking Prowess', 'High-Pressing Havoc', 'Defensive Fortress',
#               'Wing Dominance', 'Possession with Purpose', 'Youthful Energy and High Intensity',
#               'Midfield Maestros']
game_styles = {'Counter-Attacking Prowess': 'Real Madrid', 'High-Pressing Havoc': 'Liverpool', 'Defensive Fortress': 'Tottenham',
               'Wing Dominance': 'FC Bayarn', 'Possession with Purpose': 'Barcelona', 'Youthful Energy and High Intensity': 'RB Leipzig',
               'Midfield Maestros': 'Man City'}

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

col1, col2 , col3= st.columns(3)

with col1:
    option0_club_name1 = st.text_input('Club name:', '')
    option3_ages_min = st.selectbox('Minimum age', ages_min)

    option5_market_value = st.number_input('Market value', step=1_000_000)


with col2:
    #option0_club_name2 = st.text_input('Club playing style:', 'Man City')  # To be removed later
    option1_game_style = st.selectbox('Game style', options=list(game_styles.keys()))
    option4_ages_max = st.selectbox('Maximum age', ages_max)

    #option6_expected_market_value = st.number_input('Expected market value')

with col3:
    option2_selected_position = st.selectbox('Position', options=list(position_to_file.keys()))

# Display the selected parameters
filtered_df = pd.DataFrame({
    'Game style': [option1_game_style],
    'Position': [option2_selected_position],
    'Age min': [option3_ages_min],
    'Age max': [option4_ages_max],
    'Market value': [option5_market_value],
})
#'Expected market value': [option6_expected_market_value] -> AJOUTER AU MODELE SI ON VEUT

#st.write('Player parameters:')
#st.write(filtered_df)



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
        result = result.clip(lower=0.06, upper=0.11)
        result['scaled_total_score'] = abs(total_score)
        name = pd.DataFrame(data=["Nino_M"], columns=['name'])
        result = name.join(result)
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
    Ninos = Nino.join(final_df, how='cross')
    series = pd.Series([f'Nino_M_{i}' for i in range(24)])
    Ninos.name = series
    Ninos = Ninos[Ninos.goalkeepers != 1]
    Ninos.drop(columns=['goalkeepers', 'goalkeeping_abilities'], inplace=True)
    Ninos.reset_index(inplace=True, drop=True)
    data = Ninos
    #if player_name not in data['name'].values:
    #r    return f"Player '{player_name}' not found in the dataset."
    feature_columns = data.columns.drop('name')
    results = []
    for player_name in Ninos.name:
        # Extract the specified player's statistics
        player_stats = data[data['name'] == player_name].drop(columns='name')
        player_stats['label'] = km.predict(player_stats)
        # Drop the 'label' column before fitting the model
        # player_stats = player_stats.drop(columns='label')
        # Fit the NearestNeighbors model
        # Find the nearest neighbors
        distances, indices = nbrs.kneighbors(player_stats, n_neighbors= num_neighbors)
        # Get the names of similar players
        # Exclude the first one if it's the player themselves
        similar_players_indices = indices.flatten()
        similar_players_distances = distances.flatten()
        similar_players = scaled_df_kmeans.iloc[similar_players_indices]
        similar_players['distance'] = similar_players_distances
        # Sort by distance in ascending order (closer first)
        similar_players = similar_players.sort_values(by='distance', ascending=True)

        #by='scaled_total_score' bPREVIOUS SORTING
        results.append(similar_players)
    final_result = pd.concat(results)
    final_result = pd.merge(perfect_df, final_result, left_index=True, right_index=True, how='inner')
    final_result = final_result[final_result['current_age'] > option3_ages_min]
    final_result = final_result[final_result['current_age'] < option4_ages_max]
    final_result = final_result[final_result['value'] <= option5_market_value]
    surprise_du_chef = final_result
    surprise_du_chef = surprise_du_chef[surprise_du_chef[f'{option2_selected_position}_x'] != 1]
    surprise_du_chef = surprise_du_chef[surprise_du_chef['goalkeeper'] != 1]
    surprise_du_chef = surprise_du_chef[surprise_du_chef['value'] > 500_000]
    final_result = final_result[final_result[f'{option2_selected_position}_x']== 1]

    #final_result = final_result[final_result['xmv'] <= option6_expected_market_value]


    return Nino.drop(columns=['name']), final_result.sort_values(by='scaled_total_score', ascending=False), surprise_du_chef.sort_values(by='scaled_total_score', ascending=True).drop_duplicates()

# Define the subset of features for the radar chart
radar_features = ['shooting', 'dribbling_control', 'passing_vision',
                  'tackling_interception', 'aerial_defense', 'speed_agility',
                  'strength_stamina', 'decision_making', 'work_ethic_effort',
                  'leadership', 'teamwork']


# Trigger analysis based on user input
if st.checkbox('Start player analysis'):
    # Loading animation code
    with st.spinner('Performing analysis...'):
        # Call your find_closest_players function
        player_stats, closest_players_result, pepite = find_closest_players(
            position_to_file[option2_selected_position],
            option0_club_name1,
            game_styles[option1_game_style],
            100)

    # ensure that when we click on a player for the demo he has a picture
    good_results = closest_players_result[closest_players_result['club_image'].notna() &
                                          closest_players_result['profile_image'].notna()]



    # Create and display radar charts
    for i, (index, row) in enumerate(good_results[:5].iterrows()):

        fig = go.Figure()

        # Add trace for the input player
        fig.add_trace(go.Scatterpolar(
            r=player_stats.loc[0].values,
            theta=radar_features,
            fill='toself',
            name='Nino Meessen'
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
            title=f"Comparison: {'Nino Meessen'} vs {row['name']}"
        )

        # Show the plot
        st.plotly_chart(fig, use_container_width=False, sharing="streamlit", theme="streamlit")

        # Add button for each player/chart
        if st.button(f"Choose: {row['name']}"):
            st.session_state.selected_player = row['name']
            st.session_state.player_details_data = closest_players_result
            st.session_state.player_details_05 = True
            nav_page("Player_profile")


    st.success('Player analysis done!')

if st.checkbox('Show Details of Selected Players'):
    if 'closest_players_result' in locals():
        st.markdown("""**Nearest neighbors to the fictive player's statistics**""")
        st.write(closest_players_result[["name_y","club_name",'shooting', 'dribbling_control', 'passing_vision',
                  'tackling_interception', 'aerial_defense', 'speed_agility',
                  'strength_stamina', 'decision_making', 'work_ethic_effort',
                  'leadership', 'teamwork']])
        st.markdown("""**Fictive player's statistics**""")
        st.write(player_stats)


    else:
        st.warning("Please run the analysis first to see details.")

# Allow users to download the results as CSV

if 'closest_players_result' in locals():
    csv = closest_players_result.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='closest_players.csv',
        mime='text/csv',
    )


# About section
st.markdown("""
## About this Tool
This tool is designed for football analysts and enthusiasts to find players with similar characteristics and performance metrics. By inputting a player's details and selecting specific criteria, the tool uses advanced data analysis techniques to identify comparable players and visualize their similarities.
""")

# Add any additional code or features here...

# End of Streamlit app
