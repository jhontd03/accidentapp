import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import streamlit as st

@st.cache_data
def load_data_pickle(file_path):
    """
    Loads data from a pickle file.

    Args:
        file_path (str): The path to the pickle file.

    Returns:
        pandas.DataFrame: The loaded data.
    """
    data = pd.read_pickle(file_path) 
    return data

def read_data(item, path):
    """
    Reads a CSV file from the specified path and returns the data as a pandas DataFrame.

    Args:
        item (str): The name of the CSV file to read.
        path (str): The path to the directory containing the CSV file.

    Returns:
        pandas.DataFrame: The data read from the CSV file.

    Raises:
        FileNotFoundError: If the specified CSV file is not found in the given path.
        UnicodeDecodeError: If an encoding other than "ISO-8859-1" is used and the CSV file cannot be decoded.
    """
    try:
        data = pd.read_csv(os.path.join(path, item, low_memory=False))
    except:
        data = pd.read_csv(os.path.join(path, item), encoding = "ISO-8859-1", low_memory=False)    
    return data

def data_replace(data, list_cols):
    """
    Replaces specified columns in a DataFrame with new values.

    Args:
        data (pd.DataFrame): The input DataFrame.
        list_cols (list): A list of dictionaries specifying the columns to replace and their corresponding new values.

    Returns:
        pd.DataFrame: The DataFrame with replaced values.
    """        
    data = data.replace({"STATE": list_cols[0]})
    data = data.replace({"DAY_WEEK": list_cols[1]})
    data = data.replace({"MONTH": list_cols[2]})
    data = data.replace({"WEATHER": list_cols[3]})
    data = data.replace({"ROUTE": list_cols[4]})
    data = data.replace({"LGT_COND": list_cols[5]})
    
    data = data.rename(columns={'STATE':'STATENAME'})
    data = data.rename(columns={'DAY_WEEK':'DAY_WEEKNAME'})
    data = data.rename(columns={'MONTH':'MONTHNAME'})
    data = data.rename(columns={'WEATHER':'WEATHERNAME'})
    data = data.rename(columns={'ROUTE':'ROUTENAME'})
    data = data.rename(columns={'LGT_COND':'LGT_CONDNAME'})
    
    return data

def replace_state_county_city(data_year, list_cols):
    """
    Replaces state, county, and city values in the given DataFrame with the corresponding values from the provided list.

    Args:
        data_year (DataFrame): The input DataFrame containing the data.
        list_cols (list): A list of replacement values for state, county, and city in the following order:
                          [state_values, county_values, city_values].

    Returns:
        DataFrame: A copy of the input DataFrame with the state, county, and city values replaced.
    """    
    data = data_year.copy(deep=True)
    data['CODE_STATE'] = data['STATENAME']
    data['CODE_STATE'] = data['CODE_STATE'].replace(list_cols[6])
    data['COUNTY'] = data['COUNTY'].replace(list_cols[7])
    data['CITY'] = data['CITY'].replace(list_cols[8])
    return data

def graph_hist(data: pd.DataFrame, 
               bins: int=30,
               title_fig: str='', 
               label: bool=False, 
               saveToFile: str='') -> None:
    """
    Create a histogram for each column in a pandas DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.
        bins (int, optional): The number of bins for the histogram. Default is 30.
        title_fig (str, optional): The title of the figure. Default is an empty string.
        label (bool, optional): Whether to label the histogram bars with density values. Default is False.
        saveToFile (str, optional): The filename to save the figure. If not provided, the figure will be displayed.

    Returns:
        None: This function does not return any value.
    """
    name_cols = list(data.columns)
    n_cols = int(np.sqrt(len(name_cols)))
    n_rows = int(np.ceil(len(name_cols) / n_cols))

    gs = gridspec.GridSpec(n_rows, n_cols)
    gs.update(wspace=0.1, hspace=0.25)
    scale = max(n_cols, n_rows)
    fig = plt.figure(figsize=(9.5*scale, 7.5*scale))
    fig.tight_layout()
    fig.suptitle(title_fig, fontsize=24, fontweight='bold', y=0.975)    
    
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.94,
                        wspace=0.3,
                        hspace=0.5)    
    
    for i, j in enumerate(data):
        ax = fig.add_subplot(gs[i])
        n, bins_, _ = ax.hist(data.loc[:, j], bins=bins)

        if label == True:
            label_densityHist(ax, n, bins_, y=0.025, fontsize=16, fontweight='bold')
        data_mean = data.loc[:, j].mean()
        ax.axvline(x=data_mean, label='mean', c="red", linestyle="--")
        min_ylim, max_ylim = ax.get_ylim()
        ax.text(data_mean, max_ylim*0.94, \
                'mean: {:.2f}'.format(data_mean), \
                fontsize=18, fontweight='bold')

        ax.set_title(j, fontsize=20, fontweight='bold')
        ax.tick_params(axis="both", labelsize=18, rotation=0)
        for i in range(1, len(ax.get_xticklabels())):
            ax.get_xticklabels()[i].set_fontweight("bold")
        for i in range(1, len(ax.get_yticklabels())):
            ax.get_yticklabels()[i].set_fontweight("bold")
    if saveToFile == "":
        plt.show()
    else:
        fig.savefig(saveToFile, format='png', dpi=300)


def label_densityHist(ax, n, bins, x=4, y=0.01, r=2, freq='absolute', **kwargs):
    """
    Add labels,relative value of bin, to each bin in a density histogram .
    :param ax: Object axe of matplotlib
            The axis to plot.
    :param n: list, array of int, float
            The values of the histogram bins.
    :param bins: list, array of int, float
            The edges of the bins.
    :param x: int, float
            Related the x position of the bin labels. The higher, the lower the value on the x-axis.
            Default: 4
    :param y: int, float
            Related the y position of the bin labels. The higher, the greater the value on the y-axis.
            Default: 0.01
    :param r: int
            Number of decimal places.
            Default: 2
    :param **kwargs: Text properties in matplotlib
    :return: None

    Example
    import matplotlib.pyplot as plt
    import numpy as np
    dados = np.random.randn(100)

    axe = plt.gca()
    n, bins, _ = axe.hist(x=dados, edgecolor='black')
    label_densityHist(axe,n, bins)
    plt.show()

    Reference:
    [1]https://matplotlib.org/3.1.1/api/text_api.html#matplotlib.text.Text
    """

    k = []
    # calculate the relative frequency of each bin
    for i in range(0,len(n)):
        k.append((bins[i+1]-bins[i])*n[i])
    
    # rounded
    k = np.around(k,r); #print(k)
    
    # plot the label/text to each bin
    for i in range(0, len(n)):
        x_pos = (bins[i + 1] - bins[i]) / x + bins[i]
        y_pos = n[i] + (n[i] * y)
        if n[i] != 0:
            if freq == 'absolute':
                label = str(int(n[i])) # relative frequency of each bin
            elif freq == 'relative':
                label = str(k[i])
            ax.text(x_pos, y_pos, label, kwargs)
            
def replace_name(data_sum, columns):
    """
    Replaces the column names in the given DataFrame based on the specified column type.

    Args:
        data_sum (pandas.DataFrame): The DataFrame containing the data.
        columns (str): The type of column to be replaced. Possible values: 'Month', 'Day of week'.

    Returns:
        pandas.DataFrame: The modified DataFrame with the replaced column names.
    """
    if columns == 'Month':
        data_sum['month'] = data_sum['Month']
        month_name = { 'January': 1, 'February': 2, 'March': 3, 
                       'April': 4, 'May': 5, 'June': 6, 'July': 7,
                       'August': 8, 'September': 9, 'October': 10,
                       'November': 11, 'December': 12}
        data_sum = data_sum.replace({'month': month_name})
        data_sum = data_sum.sort_values('month')
        data_sum.drop('month', axis=1, inplace=True)

    if columns == 'Day of week':    
        data_sum['day_week'] = data_sum['Day of week']
        dayweek_name = { 'Thursday': 5, 'Sunday': 1, 'Wednesday': 4,
                         'Saturday': 7, 'Tuesday': 3, 'Monday': 2, 'Friday': 6}
        data_sum = data_sum.replace({'day_week': dayweek_name})
        data_sum = data_sum.sort_values('day_week')
        data_sum.drop('day_week', axis=1, inplace=True)
    return data_sum            