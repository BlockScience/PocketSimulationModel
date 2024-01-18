import pandas as pd

""" 
Threshold Inequality Calculation Functions
"""

# Network Viability
# Threshold Inequality 1
# Also Servicer Threshold Ineqality 2
# Servicer NPV

bar_s1 = 750 # POKT Threshold Value
bar_s2 = 0.9 # Fraction of Monte Carlo Sims

def servicer_npv_gt_s1_geq_s2(df: pd.DataFrame,
                              servicer_npv_col_name = "KPI 1",
                              min_pokt_threshold: float = None,
                              frac_monte_carlo_sims: float = None) -> int:
    """
    Description: 
    """
    if min_pokt_threshold is None:
        min_pokt_threshold = bar_s1
    if frac_monte_carlo_sims is None:
        frac_monte_carlo_sims = bar_s2
    
    threshold_met = (df[servicer_npv_col_name] > min_pokt_threshold).mean() >= frac_monte_carlo_sims

    return threshold_met



# Network Viability
# Threshold Inequality 2
# Also Servicer Inequality 3
# Gateway NPV

bar_t1 = 7500 # Minimum Gateway NPV Threshold
bar_t2 = 0.9 #Monte Carlo Simulation Fraction

def gateway_npv_gt_t1_geq_t2(df: pd.DataFrame,
                              col_name = "KPI 3",
                              min_pokt_threshold: float = None,
                              frac_monte_carlo_sims: float = None) -> int:
    if min_pokt_threshold is None:
        min_pokt_threshold = bar_t1
    if frac_monte_carlo_sims is None:
        frac_monte_carlo_sims = bar_t2
    
    threshold_met = (df[col_name] > min_pokt_threshold).mean() >= frac_monte_carlo_sims

    return threshold_met

# Network Viability
# Threshold Inequality 5
# Relationship Between Circulating Supply and Available Supply

v_1 = 0.3

def ratio_circ_to_available_supply_gt_v1(df: pd.DataFrame,
                                         circ_supply_col:str = "circulating_supply",
                                         available_supply_col:str = "floating_supply",
                                         threshold_val:float = None
                                         ):
    """
    Description: 
    """
    if threshold_val is None:
        threshold_val = v_1
    threshold_met = (df[circ_supply_col]/df[available_supply_col]).mean() > threshold_val
    return threshold_met

# Network Viability
# Threshold Inequality 7
# Relationship between Inflation Rate and DAO Value Capture

bar_x1 = -1.5
bar_x2 = 0.5

def avg_net_inflation_dao_value_capture_between_bounds(df: pd.DataFrame,
                                        inflation_rate_col: str = "net_minting_rate_cummulative",
                                        dao_value_col: str = "dao_value_capture",
                                        lower_bound: float = None,
                                        upper_bound: float = None):
    """
    Description:  The average elasticity of the net inflation rate of POKT
                  with respect to DAO value capture should lie between 
                  bar_x1 and bar_x2, with bar_x2 > bar_x1
    """
    if lower_bound is None:
        lower_bound = bar_x1
    if upper_bound is None:
        upper_bound = bar_x2

    inflation_rate = (df[inflation_rate_col].diff()/df[dao_value_col].diff()).mean()
    threshold_met = (inflation_rate > lower_bound) & (inflation_rate < upper_bound)
    return threshold_met

# Network Viability
# Threshold Inequality 8
# Average Net Inflation Rate

bar_y1 = -0.1
bar_y2 = 0.05

def avg_net_inflation_rate_between_bounds(df: pd.DataFrame,
                                          inflation_col_name: str = 'net_mint_rate_cummulative',
                                          lower_bound: float = None,
                                          uppr_bound: float = None):
    """
    Description:  The average net inflation rate of POKT should fall 
                between bar_y1 and bar_y2, bar_y2 > bar_y1.
    """

    if lower_bound is None:
        lower_bound = bar_y1
    if upper_bound is None:
        upper_bound = bar_y2

    average_net_inflation_rate = df[inflation_col_name]
    thresh_met = (average_net_inflation_rate > lower_bound) & (average_net_inflation_rate < upper_bound)

    return thresh_met

# Network Viability
# Threshold Inequality 9
# DAO Value Capture is Between Bounds, At Least a Certain Fraction

bar_z1 = 0.02
bar_z2 = 0.10
bar_z3 = 0.90

def dao_value_capture_between_bounds_at_least_threshold(df: pd.DataFrame,
                                                        dao_value_capture_col: str = "dao_value_capture",
                                                        lower_bound: float = None,
                                                        upper_bound: float = None,
                                                        frac_monte_carlo_sims: float = None):
    """ 
    Description: 
    """
    if lower_bound is None:
        lower_bound = bar_z1
    if upper_bound is None:
        upper_bound = bar_z2
    if frac_monte_carlo_sims is None:
        frac_monte_carlo_sims = bar_z3
    
    lower_bound_met = (df[dao_value_capture_col] > lower_bound) 
    upper_bound_met = (df[dao_value_capture_col] < upper_bound) 
    fraction_both_met = (lower_bound_met & upper_bound_met).mean()
    threshold_met = fraction_both_met > frac_monte_carlo_sims
    return threshold_met
    



###########################################
## Define lambda functions to work with  ##
## Network Viability Scenario Thresholds ##
###########################################
#  
nvs_thresh_ineq1 = servicer_npv_gt_s1_geq_s2                                         
nvs_thresh_ineq2 = gateway_npv_gt_t1_geq_t2
nvs_thresh_ineq5 = ratio_circ_to_available_supply_gt_v1

# TODO: Finish 

nvs_thresh_ineq7 = avg_net_inflation_dao_value_capture_between_bounds
nvs_thresh_ineq8 = avg_net_inflation_dao_value_capture_between_bounds
nvs_thresh_ineq9 = dao_value_capture_between_bounds_at_least_threshold

def nvs_thresh_met(df: pd.DataFrame) -> int:
    """ 
    Calculate the total NVS thresholds met. 
    """

    nvs_thresh_funcs = [nvs_thresh_ineq1, nvs_thresh_ineq2, nvs_thresh_ineq5,
                        nvs_thresh_ineq7, nvs_thresh_ineq8, nvs_thresh_ineq8]
    nvs_thresh_met = [int(nvs_thresh_func(df)) for nvs_thresh_func in nvs_thresh_funcs]
    total_thresh_met = sum(nvs_thresh_met)
    return total_thresh_met

#######################################
## Define Servicer Viability         ##
## Threshold Inequalities, which     ##
## mostly duplicate Servicer         ## 
#######################################

bar_a1 = 0.3
bar_a2 = 0.4

def average_servicer_capital_costs_between_bounds(df: pd.DataFrame,
                                                  rewards_col_name = "KPI 1",
                                                  costs_col_name = "KPI 14",
                                                  lower_bound = 0.3,
                                                  upper_bound = 0.4):
    if lower_bound is None:
        lower_bound = bar_a1
    if upper_bound is None:
        upper_bound = bar_a2
    avg_costs_per_units_of_reward = (df["KPI 14"]/df["KPI_1"]).mean()
    bounds_met = (avg_costs_per_units_of_reward > lower_bound) & (avg_costs_per_units_of_reward < upper_bound)
    return bounds_met

svs_thresh_ineq1 = average_servicer_capital_costs_between_bounds
svs_thresh_ineq2 = nvs_thresh_ineq1
svs_thresh_ineq3 = nvs_thresh_ineq2
svs_thresh_ineq4 = nvs_thresh_ineq5
svs_thresh_ineq5 = nvs_thresh_ineq7
svs_thresh_ineq6 = nvs_thresh_ineq8
svs_thresh_ineq7 = nvs_thresh_ineq9

def svs_thresh_met(df: pd.DataFrame) -> int:
    """ 
    Calculate the total SVS thresholds met. 
    """
    svs_thresh_funcs = [svs_thresh_ineq1, svs_thresh_ineq2, svs_thresh_ineq3,
                        svs_thresh_ineq4, svs_thresh_ineq5, svs_thresh_ineq6,
                        svs_thresh_ineq7]
    svs_thresh_met = [int(svs_thresh_func(df)) for svs_thresh_func in svs_thresh_funcs]
    total_thresh_met = sum(svs_thresh_met)
    return total_thresh_met


