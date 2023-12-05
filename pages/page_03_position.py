import streamlit as st
import pandas as pd

# Mapping of positions to their corresponding CSV files
position_to_file = {
    'centerback': 'centerbacks.csv',
    'fullback': 'fullbacks.csv',
    'midfielder': 'midfielders.csv',
    'winger': 'wingers.csv',
    'striker': 'strikers.csv'
}

# User selects a position
selected_position = st.selectbox('Select a position', options=list(position_to_file.keys()))

# Load the corresponding DataFrame
file_name = position_to_file[selected_position]
dataframe_path = f'raw_data/{file_name}'
selected_df = pd.read_csv(dataframe_path)

# Now, you can use 'selected_df' for further analysis or display
st.write('Data for selected position:', selected_position)
st.dataframe(selected_df)
