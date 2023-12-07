import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
from streamlit.components.v1 import html
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
st.title("Player Profile ")
selected_player = st.session_state.selected_player
player_details = st.session_state.player_details_data
radar_features = ['shooting', 'dribbling_control', 'passing_vision',
                  'tackling_interception', 'aerial_defense', 'speed_agility',
                  'strength_stamina', 'decision_making', 'work_ethic_effort',
                  'leadership', 'teamwork']
full_player = player_details[player_details['name_y'] == selected_player]
player_image = full_player.profile_image.iloc[0]
club_image = full_player.club_image.iloc[0]
club_name = full_player.club_name.iloc[0]
value = full_player.value.iloc[0]
xmv = full_player.xmv.iloc[0]
player_stats = full_player[radar_features]
col1, col2, col3= st.columns(3)
stats_values = player_stats
with col1:
    # Display placeholder images
    st.image(player_image, caption=selected_player, width=100)
with col2:
    st.image(club_image,
        width=100,  # Set the desired width
        caption=club_name
        )  # Set the desired image format
with col3:
    st.markdown(f'''## MV: € {value} ''')
    st.markdown(f'## XMV: € {round(xmv, -3)}')
# Create a single column for stats
stats_columns = st.columns(11)
# Display stats in a horizontal layout
for i, feature in enumerate(radar_features):  # Assuming 11 stats, adjust as needed
    stats_columns[i].metric(label= feature, value=int(player_stats[feature].iloc[0] * 1000 // 1.2))
st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3NwZmhocnJleGt1dnBiY2R2YjIyN3E3ZHZuMHdnemFkZzBhcGx2ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0EoBPIfQafOYpwJy/giphy.gif", use_column_width="always")
