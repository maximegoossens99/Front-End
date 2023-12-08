import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import plotly.express as px

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

# Page title and subtitle
st.title("Player Profile")

# Player details
selected_player = st.session_state.selected_player
player_details = st.session_state.player_details_data
radar_features = ['shooting', 'dribbling_control', 'passing_vision',
                  'tackling_interception', 'aerial_defense', 'speed_agility',
                  'strength_stamina', 'decision_making', 'work_ethic_effort',
                  'leadership', 'teamwork']
full_player = player_details[player_details['name_y'] == selected_player]
player_image = full_player.profile_image.iloc[0].replace('small', 'big')
club_image = full_player.club_image.iloc[0].replace('small', 'big')
club_name = full_player.club_name.iloc[0]
value = full_player.value.iloc[0]
xmv = full_player.xmv.iloc[0]
player_stats = full_player[radar_features]

# Player details layout
col1, col2, col3 = st.columns(3)

# Column 1: Player image with border and shadow
with col1:
    st.image(player_image, width=150, output_format='JPEG', channels='RGB')
    st.markdown(
        f"<p style='text-align: left; font-size: 1.7rem; font-weight: bold; margin-top: 0px; margin-bottom: 0px;'>{selected_player}</p>",
        unsafe_allow_html=True
    )

# Column 2: Club details with border and shadow
with col2:
    st.image(club_image, width=150, output_format='JPEG', channels='RGB')
    st.markdown(
        f"<p style='text-align: left; font-size: 1.3rem; font-weight: bold; margin-top: 45px; margin-bottom: 0px;'>{club_name}</p>",
        unsafe_allow_html=True
    )

# Display Market Value
with col3:
    st.info(
        """
        ##### Market Value
        **{}**""".format(
            '€ {:.2f} M'.format(value / 1_000_000) if value >= 1_000_000 else '€ {:.2f} k'.format(value / 1_000)
        ), icon='💰'
    )

# Display XMV
with col3:
    st.info(
        """
        ##### xMarket Value
        **{}**""".format(
            '€ {:.2f} M'.format(xmv / 1_000_000) if xmv >= 1_000_000 else '€ {:.2f} k'.format(xmv / 1_000)
        ), icon='💰'
    )


# Stats layout
stats_columns = st.columns(len(radar_features))

# Create a horizontal bar chart for each metric
for i, feature in enumerate(radar_features):
    with stats_columns[i]:
        short_label = feature[:4] if len(feature) > 5 else feature
        # Calculate the percentage of the metric value
        percentage = int(player_stats[feature].iloc[0] * 1000 // 1.3)

        # Determine color based on percentage
        if percentage < 30:
            bar_color = "#FF5733"  # Red
        elif percentage < 70:
            bar_color = "#FFD700"  # Orange
        else:
            bar_color = "#4CAF50"  # Green

        # Display the label, colored bar, and value using HTML
        st.markdown(
            f"<p style='text-align: center; margin: 0px; font-size: 1rem; font-weight: bold;'>{short_label}</p>"
            f"<div style='background-color: #e0e0e0; border-radius: 5px; height: 20px; margin-bottom: 5px;'>"
            f"<div style='background-color: {bar_color}; width: {percentage}%; height: 100%; border-radius: 5px;'></div>"
            f"</div>"
            f"<p style='text-align: center; margin: 10px; font-size: 1.0rem;'>{player_stats[feature].iloc[0]* 1000 // 1.3}</p>",
            unsafe_allow_html=True
        )



st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3NwZmhocnJleGt1dnBiY2R2YjIyN3E3ZHZuMHdnemFkZzBhcGx2ayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0EoBPIfQafOYpwJy/giphy.gif", use_column_width="always")
