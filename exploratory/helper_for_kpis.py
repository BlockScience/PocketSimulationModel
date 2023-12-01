import pandas as pd

############################################
## Helper functions for KPIs              ##
############################################

def calculate_gini_from_list(values: list[float] == None) -> float:
    """
    Calculate the Gini coefficient from a list of values.

    Parameters:
    -----------
    values : list
        A list of floats representing the data points for which 
        the Gini coefficient is to be calculated.

    Returns:
    --------
    float
        The Gini coefficient calculated from the data.
    """

    if values is None:
        return 0.0 

    else: 
        n = len(values)

    # Handle case where values list is empty or all values are zero
    if n == 0:
        return 0.0

    x_bar = sum(values) / n

    # Calculating the sum of absolute differences
    sum_of_differences = sum(abs(j - k) for j in values for k in values)

    # Calculating the Gini coefficient
    gini = sum_of_differences / (2 * n**2 * x_bar)

    return gini

def calculate_gini_from_dict(dict_to_use: dict = None) -> float:
    """
    Calculate the Gini coefficient from a list of values.

    Parameters:
    -----------
    values : list
        A list of floats representing the data points for which 
        the Gini coefficient is to be calculated.

    Returns:
    --------
    float
        The Gini coefficient calculated from the data.
    """

    if dict_to_use is None:
        return 0.0

    values = dict_to_use.values()
    gini = calculate_gini_from_list(values)
    return gini

def KPI_C(df: pd.DataFrame,
         col_name: str) -> float:
    """
    KPI-C is the average Gini coefficient over the entries in the column.
    """
    filtered_df = df[df[col_name].apply(lambda x: not(x is None))]
    num_entries = filtered_df.shape[0]
    total_gini_coeff = sum(filtered_df[col_name].apply(lambda x: calculate_gini_from_dict(x)))
    average_gini_coeff = total_gini_coeff/num_entries
    return average_gini_coeff





