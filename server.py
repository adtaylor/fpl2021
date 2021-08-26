import requests
import streamlit as st
import pandas as pd
import numpy as np

FPL_URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

@st.cache
def load_data():
    r = requests.get(FPL_URL)
    json = r.json()
    elements_df = pd.DataFrame(json['elements'])
    elements_types_df = pd.DataFrame(json['element_types'])
    teams_df = pd.DataFrame(json['teams'])
    slim_elements_df = elements_df[['second_name','team','element_type','value_season','total_points', 'now_cost']]
    slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
    slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
    slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
    slim_elements_df = slim_elements_df.drop(columns=['element_type', 'value_season'])
    slim_elements_df.style.hide_index()
    slim_elements_df.sort_values('value',ascending=False)
    slim_elements_df = slim_elements_df.loc[slim_elements_df.value > 0]
    return slim_elements_df


st.title('FPL 2021 Docs')

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

pivot = data.pivot_table(index='position',values='value',aggfunc=np.mean).reset_index()
st.dataframe( pivot.sort_values('value',ascending=False) )
