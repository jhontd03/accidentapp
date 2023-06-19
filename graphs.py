import pandas as pd
import plotly.express as px
from common import replace_name
import streamlit as st
import pydeck as pdk 

@st.cache_data
def count_graph(data, state_filter, year_filter, cat_filter):    
    """
    Generate a bar graph showing the total accidents based on filters.

    Parameters:
    - data: Pandas DataFrame containing accident data
    - state_filter: Filter for specific state(s) (string or list of strings)
    - year_filter: Filter for specific year(s) (string or list of strings)
    - cat_filter: Filter for specific category (string)

    Returns:
    - fig_count: (plotly.graph_objects.Figure): bar graph figure.
    """
    
    if isinstance(state_filter, list) == False:
        state_filter = [state_filter]

    if isinstance(year_filter, list) == False:
        year_filter = [year_filter]
    year_filter = [int(item) for item in year_filter]
               
    year_count = data[(data['State'].isin(state_filter)) & (data['Year'].isin(year_filter))][cat_filter].value_counts().to_frame().reset_index()
    year_count.columns = [cat_filter, 'Total accidents']

    year_count = replace_name(year_count, cat_filter)
    
    if cat_filter == 'City':
        year_count = year_count[year_count[cat_filter] != "Not Applicable"]

    if cat_filter in ['State', 'County', 'City']:
        year_count = year_count.sort_values(by='Total accidents', ascending=False).head(20)
          
    fig_count = px.bar(year_count, 
                      x=cat_filter, 
                      y='Total accidents', 
                      width=900, 
                      height=600,
                       color_discrete_sequence = ['#2e62f2'],
                       text=[f'{i}' for i in year_count['Total accidents']]
                      )
    fig_count.update_traces(textfont_color='#f2f4fa',
                            textposition='outside')

    fig_count.update_layout(
        margin=dict(l=30, r=30, t=30, b=20),
        paper_bgcolor="#18181a",
        font=dict(family = 'sans-serif', color='#f2f4fa', size=14),
        plot_bgcolor='#18181a',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        hoverlabel_font_color='#f2f4fa'
    )
    return fig_count


@st.cache_data
def scatter_graph(data, year_filter, state_filter, x_var, y_var, z_var): 

    """
    Generates a scatter graph based on the provided data and filters.

    Parameters:
    - data (pandas.DataFrame): The input data containing the required columns.
    - year_filter (int or list): The year(s) to filter the data by.
    - state_filter (str or list): The state(s) to filter the data by.
    - x_var (str): The column name representing the x-axis variable.
    - y_var (str): The column name representing the y-axis variable.
    - z_var (str): The column name representing the size variable for markers.

    Returns:
    - fig_scatter (plotly.graph_objects.Figure): Scatter graph figure.
    """
    
    if isinstance(year_filter, list) == False:
        year_filter = [year_filter]
    year_filter = [int(item) for item in year_filter]
    year_filter = tuple(year_filter)
    
    if isinstance(state_filter, list) == False:
        state_filter = [state_filter]
                
    data = data[(data['State'].isin(state_filter))]
    
    fig_scatter = px.scatter(
        data.query(f'Year in {year_filter}'),
        x=x_var,
        y=y_var,
        size=z_var,
        color="State",
        size_max=60,
        width=800, 
        height=400)

    fig_scatter.update_layout(
        margin=dict(l=30, r=30, t=30, b=20),
        paper_bgcolor="#18181a",
        font=dict(family = 'sans-serif', color='#f2f4fa', size=12),
        plot_bgcolor='#18181a',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        hoverlabel_font_color='#f2f4fa'
    ) 
    return fig_scatter

# @st.cache_data
def map_accident(data, state_filter, year_filter, var_filter):
    """
    Generates a map visualization of accidents using the specified data and filters.

    Args:
        data (pandas.DataFrame): The data to be used for the map visualization.
        state_filter (str or list): The state or states to filter the data by.
        year_filter (int or list): The year or years to filter the data by.
        var_filter (str): The variable used to determine the elevation range of the markers.

    Returns:
        None
    """    

    if isinstance(state_filter, list) == False:

        if isinstance(year_filter, list) == False:
            year_filter = [year_filter]
        year_filter = [int(item) for item in year_filter]
        
        data_filter = data[(data['State'].isin([state_filter])) & (data['Year'].isin(year_filter))]
    
        val_min = data_filter[var_filter].min()
        val_max = data_filter[var_filter].max()
        
        data_filter = data_filter.rename(columns={'longitud': 'longitude'})
        data_filter = data_filter.loc[:, ['latitude', 'longitude']]
        
        val_long = data_filter['longitude'].describe().iloc[5]
        val_lat = data_filter['latitude'].describe().iloc[5]
        
        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/dark-v11',
            initial_view_state=pdk.ViewState(
                latitude=val_lat,
                longitude=val_long,
                zoom=6.5,
                min_zoom=5,
                max_zoom=15,
                pitch=45,
                bearing=-45
            ),
            layers=[
                pdk.Layer(
                  'HexagonLayer',
                   data=data_filter,
                   get_position='[longitude, latitude]',
                   radius=200,
                   elevation_scale=500,
                   elevation_range=[val_min, val_max],
                   pickable=True,
                   extruded=True,
                    auto_highlight=False,
                ),
                pdk.Layer(
                   'ScatterplotLayer',
                    data=data_filter,
                    get_position='[longitude, latitude]',
                    get_color='[180, 0, 200, 140]',
                    get_radius=200,
                    auto_highlight=True,
                ),
            ],
        ))


@st.cache_data        
def sum_stats_study(data, state_filter, year_filter, study_stats, cat_filter):
    """
    Calculates and visualizes summary statistics based on specified filters.

    Args:
        data (pandas.DataFrame): The data used for the analysis.
        state_filter (str or list): The state or states to filter the data by.
        year_filter (int or list): The year or years to filter the data by.
        study_stats (str): The statistics to be calculated.
        cat_filter (str): The category used for grouping the data.

    Returns:
        plotly.graph_objects.Figure: The bar chart figure.
    """

    if isinstance(state_filter, list) == False:
        state_filter = [state_filter]

    if isinstance(year_filter, list) == False:
        year_filter = [year_filter]
    year_filter = [int(item) for item in year_filter]
    
    sum_stats = data[(data['Year'].isin(year_filter)) & (data['State'].isin(state_filter))].groupby([cat_filter]).sum(numeric_only=True)[study_stats]

    sum_stats = pd.DataFrame(sum_stats)
    sum_stats.reset_index(inplace=True)        

    sum_stats = replace_name(sum_stats, cat_filter)

    if cat_filter == 'City':
        sum_stats = sum_stats[sum_stats[cat_filter] != "Not Applicable"]
      
    if cat_filter in ['State', 'County', 'City']:
        sum_stats = sum_stats.sort_values(by=study_stats, ascending=False).head(20)

    fig_sum = px.bar(sum_stats, 
                      x=cat_filter, 
                      y=study_stats, 
                      width=600, 
                      height=500,
                      text=[f'{i}' for i in sum_stats[study_stats]],
                      color_discrete_sequence =['#AD8317'])

    fig_sum.update_traces(textfont_color='#f2f4fa',
                            textposition='outside')

    fig_sum.update_layout(
        margin=dict(l=60, r=20, t=60, b=80),
        paper_bgcolor="#18181a",
        font=dict(family='sans-serif', color='#f2f4fa', size=14),
        plot_bgcolor='#18181a',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        hoverlabel_font_color='#f2f4fa'
    )
    
    return fig_sum

@st.cache_data
def choropleth_graph(data, year_filter, var_filter):
    """
    Generates a choropleth graph using the specified data and filters.

    Args:
        data (pandas.DataFrame): The data to be used for the choropleth graph.
        year_filter (int or list): The year or years to filter the data by.
        var_filter (str): The variable to be plotted on the choropleth map.

    Returns:
        plotly.graph_objects.Figure: The choropleth graph figure.
    """    

    if isinstance(year_filter, list) == False:
        year_filter = [year_filter]
    year_filter = [int(item) for item in year_filter]
    
    code_state = data['code_state'].unique()
    name_state = data['State'].unique()
    code_name = dict(zip(name_state, code_state))

    data_mean = data[(data['Year'].isin(year_filter))].groupby('State').mean(numeric_only=True).reset_index()
    
    data_mean['code_state'] = data_mean['State']
    data_mean['code_state'] = data_mean['code_state'].replace(code_name)

    fig_map = px.choropleth(data_mean,
                            locations='code_state',
                            color=var_filter,
                            color_continuous_scale='hot',
                            hover_name='State',
                            locationmode='USA-states',
                            scope='usa')

    fig_map.update_layout(
        margin=dict(l=30, r=30, t=30, b=20),
        paper_bgcolor="#18181a",
        font=dict(family = 'sans-serif', color='#f2f4fa', size=14),
        plot_bgcolor='#18181a',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        hoverlabel_font_color='#f2f4fa',
        geo=dict(bgcolor='#18181a')
    )

    return fig_map